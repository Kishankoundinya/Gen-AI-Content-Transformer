# Gen AI Content Transformer

An offline, AI-powered platform that converts source text into multiple professional output formats. Uses **TinyLlama-1.1B-Chat-v1.0** (quantized via llama.cpp) running fully on your machine. No API keys, no cloud, no data leaves your computer.

## Architecture

- **Backend** — Python FastAPI server that hosts the model and a JSON API
- **Frontend** — Modern React dashboard (built with Vite), served by the backend
- **Inference** — `llama.cpp` with a Q4_K_M quantized model (~700MB) for fast CPU inference. On Apple Silicon this uses Metal acceleration and is several times faster than the PyTorch FP32 approach.

## Features

- **100% Offline** — All inference is local after setup
- **7 Output Formats** — Video package, LinkedIn post, Twitter/X post, Advisory, Infographic, Executive Summary, Presentation
- **Multi-format Generation** — Generate several formats from one source in a single pass
- **Flexible Input** — Paste text or upload `.txt` / `.md` files
- **Configurable Parameters** — Target audience, tone, language, detail level, objective, style, and sampling controls
- **Downloadable Outputs** — Export individual or combined results as Markdown
- **Fast on CPU** — Quantized model runs several times faster than unquantized PyTorch inference

## Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.9 or higher |
| Node.js | 18 or higher (only needed at setup time to build the UI) |
| RAM | 4 GB minimum (8 GB recommended) |
| Disk | 4 GB free |
| OS | macOS, Linux, Windows (WSL2) |

## Quick Start

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/GenAi_Based_content_Transformer.git
cd GenAi_Based_content_Transformer
```

### 2. Setup

```bash
chmod +x setup.sh run.sh
./setup.sh
```

This creates a Python virtual environment, installs backend dependencies, **downloads the quantized model once (~700MB)**, installs frontend dependencies, and builds the React UI.

> The model is downloaded during setup, so generation is fast immediately after install.

### 3. Run

```bash
./run.sh
```

Open **http://localhost:8000** in your browser.

The whole app runs from a single server: the FastAPI backend serves both the JSON API and the built React dashboard.

## Development Mode

For live frontend reloading during development:

```bash
./run.sh --dev
```

- Backend runs on `http://localhost:8000`
- Vite dev server runs on `http://localhost:5173` and proxies `/api` to the backend

## Usage

1. **Paste or upload source content** in the left panel.
2. **Select one or more output formats** (tiles toggle on/off).
3. **Adjust parameters** — audience, tone, language, level of detail, objective, style, max tokens, temperature, top-p.
4. Click **Generate Content**. Each selected format is generated in sequence with a progress indicator.
5. **Review results** in the right panel and **Download** the ones you want.

### Output Types

| Output Type | What It Generates |
|---|---|
| Video | Script, storyboard, scene descriptions, narration, subtitles, visual recommendations |
| LinkedIn Post | Professional post ready to publish |
| Twitter/X Post | Single tweet + tweet thread + engagement tweet |
| Advisory | Structured advisory with findings, risks, recommendations |
| Infographic | Content sections, layout recommendations, key messaging |
| Executive Summary | Concise briefing with key points, recommendations, next steps |
| Presentation | Slide-by-slide content with speaker notes and design tips |

## Backend API

| Endpoint | Method | Description |
|---|---|---|
| `/api/health` | GET | Backend + model status |
| `/api/model-info` | GET | Active backend and model details |
| `/api/output-types` | GET | Available output types |
| `/api/generate` | POST | Generate one output type |

Example:

```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "output_type": "LinkedIn Post",
    "source_content": "Our company reduced costs by 30% using AI automation...",
    "tone": "Professional",
    "max_new_tokens": 1024
  }'
```

## Project Structure

```
GenAi_Based_content_Transformer/
├── backend/
│   ├── api.py                # FastAPI server + static frontend serving
│   ├── model_service.py      # llama.cpp primary, transformers fallback
│   ├── hub_download.py       # Downloads quantized model during setup
│   ├── prompt_templates.py   # Prompts for each output type
│   ├── output_generators.py  # Generation orchestration
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── index.html
│   ├── vite.config.js        # Dev proxy to backend
│   ├── package.json
│   └── src/
│       ├── App.jsx           # Main dashboard
│       ├── styles.css        # Styling
│       ├── services/api.js   # Backend API client
│       └── components/
│           ├── InputPanel.jsx          # Step 1: source content
│           ├── OutputTypeSelector.jsx  # Step 2: output types
│           ├── ParametersPanel.jsx     # Step 3: parameters
│           └── OutputPanel.jsx         # Results + download
├── models/                   # Downloaded GGUF model (created by setup)
├── setup.sh                  # One-command setup
├── run.sh                    # Launch the app
├── .gitignore
└── README.md
```

## Platform Notes

| Platform | Inference Backend | Notes |
|---|---|---|
| macOS (Apple Silicon) | llama.cpp with Metal | Fastest on Mac |
| Linux (with NVIDIA GPU) | llama.cpp (CUDA build) | Fastest overall |
| Linux (CPU) | llama.cpp | Fast, quantized CPU inference |
| Windows (WSL2 + NVIDIA) | llama.cpp (CUDA build) | Requires WSL2 |

If `llama-cpp-python` cannot be installed, the app automatically falls back to a Hugging Face `transformers` backend (slower but functional).

## Troubleshooting

**Setup fails while installing `llama-cpp-python`:**
The base install may require compilation on some platforms. The setup script retries automatically. If it still fails, the app falls back to the `transformers` backend:
```bash
./setup.sh
```

**Model download fails:**
You need internet for the one-time model download. After that the app works fully offline.

**Slow generation:**
- Reduce `Max Output Tokens` (256-384 is usually plenty)
- Generate one output type at a time instead of several
- Use shorter source content (context window is 2048 tokens total)
- `llama.cpp` Metal/CUDA builds are significantly faster than CPU

**Empty or poor-quality output:**
- Try shorter source content
- Lower `Temperature` for more focused output (e.g., 0.5)
- The 1.1B model cannot handle extremely complex instructions; keep source content focused

**Port already in use:**
```bash
./run.sh  # editing PORT? Use:
uvicorn backend.api:app --host 0.0.0.0 --port 8501
```

**Clear cached model and rebuild:**
```bash
rm -rf models/
rm -rf .venv frontend/node_modules frontend/dist
./setup.sh
```

## License

The TinyLlama model is licensed under [Apache 2.0](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0/blob/main/LICENSE).