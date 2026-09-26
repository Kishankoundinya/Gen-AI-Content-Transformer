"""
Model service for local inference.

Primary backend: llama.cpp (GGUF quantized TinyLlama)
  - Much faster on CPU (and uses Metal on Apple Silicon)
  - ~700MB model instead of ~2.2GB
Fallback backend: Hugging Face transformers (FP32 on CPU)

The GGUF model is downloaded during setup so the app is fast after install.
"""

import os
import glob
import threading
from .hub_download import ensure_model_downloaded

MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models")

_lock = threading.Lock()
_model = None
_model_backend = None


def _resolve_gguf_path():
    """Find the downloaded GGUF model file or return None."""
    models_dir = os.path.abspath(MODEL_DIR)
    candidates = list(glob.glob(os.path.join(models_dir, "**", "*.gguf"), recursive=True))
    if candidates:
        return candidates[0]
    return None


def _load_llamacpp():
    """Try to load model via llama-cpp-python. Returns (model, backend_name) or (None, None)."""
    try:
        from llama_cpp import Llama

        path = _resolve_gguf_path()
        if not path:
            return None, None

        n_threads = max(2, (os.cpu_count() or 4))
        model = Llama(
            model_path=path,
            n_ctx=2048,
            n_threads=n_threads,
            n_batch=128,
            verbose=False,
        )
        return model, "llama.cpp (GGUF Q4_K_M)"
    except Exception:
        return None, None


def _load_transformers():
    """Fallback: load via Hugging Face transformers."""
    try:
        import torch
        import platform
        from transformers import AutoModelForCausalLM, AutoTokenizer

        model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        if torch.cuda.is_available():
            kwargs = {"device_map": "auto", "torch_dtype": torch.float16}
        elif platform.system() == "Darwin" and torch.backends.mps.is_available():
            kwargs = {"device_map": "cpu", "torch_dtype": torch.float32}
        else:
            kwargs = {"device_map": "cpu", "torch_dtype": torch.float32}

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name, low_cpu_mem_usage=True, **kwargs)
        model.eval()
        return (model, tokenizer), "transformers (FP32 CPU)"
    except Exception:
        return None, None


def load_model():
    """Load the model once (thread-safe). Prioritizes llama.cpp for speed."""
    global _model, _model_backend
    if _model is not None:
        return _model, _model_backend

    with _lock:
        if _model is not None:
            return _model, _model_backend

        model, backend = _load_llamacpp()
        if model is not None:
            _model, _model_backend = model, backend
            return _model, _model_backend

        fallback, backend = _load_transformers()
        if fallback is not None:
            _model, _model_backend = fallback, backend
            return _model, _model_backend

        raise RuntimeError(
            "No model backend available. Install llama-cpp-python or transformers."
        )


def unload_model():
    """Free the model from memory."""
    global _model, _model_backend
    _model = None
    _model_backend = None


def _build_chat_prompt(prompt: str) -> str:
    """Wrap a user prompt in TinyLlama's chat format."""
    return (
        "<|system|>\n"
        "You are a professional content creator and writer. "
        "You produce high-quality, well-structured content based on user instructions.</s>\n"
        "<|user|>\n"
        f"{prompt}</s>\n"
        "<|assistant|>\n"
    )


def generate_text(
    prompt: str,
    max_new_tokens: int = 1024,
    temperature: float = 0.7,
    top_p: float = 0.9,
) -> str:
    """Generate text using whatever backend is available."""
    model, backend = load_model()
    formatted_prompt = _build_chat_prompt(prompt)

    if backend.startswith("llama.cpp"):
        return _generate_llamacpp(model, formatted_prompt, max_new_tokens, temperature, top_p)
    else:
        return _generate_transformers(model, formatted_prompt, max_new_tokens, temperature, top_p)


def _generate_llamacpp(model, prompt, max_new_tokens, temperature, top_p):
    response = model(
        prompt,
        max_tokens=max_new_tokens,
        temperature=temperature,
        top_p=top_p,
        top_k=50,
        repeat_penalty=1.1,
        stop=["</s>", "<|user|>", "<|assistant|>"],
        echo=False,
    )
    return response["choices"][0]["text"].strip()


def _generate_transformers(model, prompt, max_new_tokens, temperature, top_p):
    import torch
    model_obj, tokenizer = model

    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    input_ids = input_ids.to(model_obj.device)

    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id

    with torch.no_grad():
        outputs = model_obj.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=50,
            repetition_penalty=1.1,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )

    generated = outputs[0][input_ids.shape[1]:]
    return tokenizer.decode(generated, skip_special_tokens=True).strip()


def get_model_info() -> dict:
    """Return info about the active backend."""
    try:
        _, backend = load_model()
        backend_name = backend
    except Exception:
        backend_name = "not loaded"

    return {
        "name": "TinyLlama-1.1B-Chat-v1.0",
        "parameters": "~1.1 Billion",
        "architecture": "LLaMA 2 based",
        "backend": backend_name,
        "context_window": "2048 tokens",
    }