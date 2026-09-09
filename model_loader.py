"""
Model loader for TinyLlama local inference.
Handles downloading, caching, and generating text with TinyLlama-1.1B-Chat-v1.0.
"""

import torch
import platform
from transformers import AutoModelForCausalLM, AutoTokenizer
import streamlit as st
import gc


MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
MAX_CONTEXT_LENGTH = 2048


def _get_device_config():
    """Determine the best device config. Avoid MPS on macOS due to unsupported ops."""
    if torch.cuda.is_available():
        return {"device_map": "auto", "torch_dtype": torch.float16}
    elif torch.backends.mps.is_available() and platform.system() == "Darwin":
        # MPS has unsupported ops for TinyLlama — force CPU with float32
        return {"device_map": "cpu", "torch_dtype": torch.float32}
    else:
        return {"device_map": "cpu", "torch_dtype": torch.float32}


@st.cache_resource(show_spinner="Loading TinyLlama model... This may take a few minutes on first run.")
def load_model():
    """Load TinyLlama model and tokenizer with caching."""
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    config = _get_device_config()
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=config["torch_dtype"],
        device_map=config["device_map"],
        low_cpu_mem_usage=True,
    )
    model.eval()
    return model, tokenizer


def unload_model():
    """Free model from memory."""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    gc.collect()


def generate_text(
    prompt: str,
    max_new_tokens: int = 1024,
    temperature: float = 0.7,
    top_p: float = 0.9,
    top_k: int = 50,
    repetition_penalty: float = 1.1,
    do_sample: bool = True,
) -> str:
    """
    Generate text using the loaded TinyLlama model.

    Truncates the prompt if it exceeds the model's context window,
    reserving space for generation.
    """
    model, tokenizer = load_model()

    formatted_prompt = (
        "<|system|>\n"
        "You are a professional content creator and writer. "
        "You produce high-quality, well-structured content based on user instructions.</s>\n"
        "<|user|>\n"
        f"{prompt}</s>\n"
        "<|assistant|>\n"
    )

    # Tokenize and check length
    input_ids = tokenizer.encode(formatted_prompt, return_tensors="pt")
    input_length = input_ids.shape[1]

    # Reserve space for generation
    available_tokens = MAX_CONTEXT_LENGTH - max_new_tokens - 10  # 10 for safety margin

    if input_length > available_tokens:
        # Truncate from the middle of the user content to keep system prompt and structure
        system_and_user_start = tokenizer.encode(
            "<|system|>\nYou are a professional content creator and writer. "
            "You produce high-quality, well-structured content based on user instructions.</s>\n"
            "<|user|>\n",
            return_tensors="pt",
        ).shape[1]
        assistant_header = tokenizer.encode("<|assistant|>\n", return_tensors="pt").shape[1]

        # Keep system prompt + user start + user end + assistant header
        truncation_reserve = system_and_user_start + assistant_header + max_new_tokens + 20
        if input_length > truncation_reserve:
            # Keep first part and end of user content
            keep_from_start = system_and_user_start + 20
            keep_from_end = input_length - truncation_reserve + keep_from_start
            user_content_start = input_ids[:, :keep_from_start]
            user_content_end = input_ids[:, keep_from_end:]
            # Add truncation notice
            truncation_notice = tokenizer.encode(
                "\n[Content truncated for context window]</s>\n",
                return_tensors="pt",
                add_special_tokens=False,
            )
            input_ids = torch.cat([user_content_start, truncation_notice, user_content_end], dim=1)

    # Move to same device as model
    input_ids = input_ids.to(model.device)

    # Set pad token
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id

    with torch.no_grad():
        outputs = model.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            repetition_penalty=repetition_penalty,
            do_sample=do_sample,
            pad_token_id=tokenizer.eos_token_id,
        )

    generated = outputs[0][input_ids.shape[1]:]
    result = tokenizer.decode(generated, skip_special_tokens=True)
    return result.strip()


def get_model_info() -> dict:
    """Return info about the loaded model."""
    return {
        "name": MODEL_NAME,
        "parameters": "~1.1 Billion",
        "architecture": "LLaMA 2 based",
        "quantization": "FP16",
        "max_context": f"{MAX_CONTEXT_LENGTH} tokens",
    }
