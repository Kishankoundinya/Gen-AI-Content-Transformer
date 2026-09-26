"""
Downloads the quantized TinyLlama GGUF model from Hugging Face Hub.
Downloads during setup so the app is fast after install.
"""

import os
import glob
import sys
from pathlib import Path

BBASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BBASE_DIR, "models")

GGUF_REPO = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"
PREFERRED_FILE = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"


def have_model() -> bool:
    """Check if a GGUF model is already downloaded."""
    if not os.path.isdir(MODEL_DIR):
        return False
    return any(glob.glob(os.path.join(MODEL_DIR, "**", "*.gguf"), recursive=True))


def ensure_model_downloaded(force: bool = False) -> str:
    """Download the GGUF model if not present. Returns path to the model."""
    if not force and have_model():
        existing = glob.glob(os.path.join(MODEL_DIR, "**", "*.gguf"), recursive=True)
        if existing:
            return existing[0]

    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        sys.exit(
            "huggingface_hub is not installed. Run: pip install huggingface-hub"
        )

    Path(MODEL_DIR).mkdir(parents=True, exist_ok=True)

    print(f"Downloading model: {GGUF_REPO} ({PREFERRED_FILE}) ...")
    path = hf_hub_download(
        repo_id=GGUF_REPO,
        filename=PREFERRED_FILE,
        local_dir=MODEL_DIR,
    )
    print(f"Model downloaded to {path}")
    return path


if __name__ == "__main__":
    path = ensure_model_downloaded()
    print(f"Model ready: {path}")