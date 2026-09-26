#!/bin/bash
# Gen AI Content Transformer - Setup Script
# Installs backend (Python) + frontend (React) dependencies
# and downloads the quantized model once so the app runs fast.

set -e

echo "========================================="
echo " Gen AI Content Transformer - Setup"
echo "========================================="
echo ""

PYTHON="${PYTHON:-python3}"

# ── 1. Python checks ──────────────────────────────────────────────────────────
echo "1/4 Python environment"
echo "Checking: $("$PYTHON" --version 2>&1 || echo 'python3 not found')"
if ! command -v "$PYTHON" >/dev/null 2>&1; then
    echo "ERROR: python3 is required. Install Python 3.9+ first." >&2
    exit 1
fi

# ── 2. Virtual environment + backend deps ────────────────────────────────────
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    "$PYTHON" -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip --quiet

echo "Installing backend dependencies..."
pip install -r backend/requirements.txt --quiet || true

# llama-cpp-python may need compilation depending on platform. Retry with
# Metal enabled on macOS if it did not install.
if ! python -c "import llama_cpp" >/dev/null 2>&1; then
    echo "llama-cpp-python base install failed. Trying Metal-enabled build (macOS)..."
    CMAKE_ARGS="-DGGML_METAL=on" pip install --force-reinstall llama-cpp-python --quiet || \
        echo "WARNING: llama-cpp-python not available; falling back to transformers backend."
fi

# ── 3. Download the quantized model ───────────────────────────────────────────
echo ""
echo "2/4 Model download"
python -m backend.hub_download || python backend/hub_download.py
if ! python -c "import torch" >/dev/null 2>&1; then
    echo "torch not available; installing (required for fallback backend)..."
    pip install "torch>=2.0.0" --quiet || echo "WARNING: torch install failed; llama.cpp backend will be used if present."
fi

# ── 4. Frontend build ─────────────────────────────────────────────────────────
echo ""
if command -v npm >/dev/null 2>&1; then
    echo "3/4 Installing frontend dependencies (npm install)..."
    (cd frontend && npm install --silent)
    echo "Building frontend..."
    (cd frontend && npm run build)
else
    echo "WARNING: npm not found. The React frontend will not be built."
    echo "         Install Node.js (v18+) and rerun ./setup.sh to build the UI."
fi

# ── Config check ─────────────────────────────────────────────────────────────
if [ -f ".streamlit/config.toml" ]; then
    rm -f .streamlit/config.toml
fi

echo ""
echo "========================================="
echo " Setup Complete"
echo "========================================="
echo ""
echo "To run the application:"
echo ""
echo "   ./run.sh"
echo ""
echo "Then open http://localhost:8000 in your browser"
echo ""
echo "For development (frontend hot reload):"
echo "   ./run.sh --dev"
echo ""