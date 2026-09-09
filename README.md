# Gen AI Content Transformer

An offline, AI-powered content transformation platform that converts source text into multiple professional output formats using **TinyLlama-1.1B-Chat-v1.0** running locally on your machine. No API keys, no internet required after setup.

## Features

- **100% Offline** — All inference runs locally using TinyLlama; no data leaves your machine
- **7 Output Formats** — Video package, LinkedIn post, Twitter/X post, Advisory, Infographic, Executive Summary, Presentation
- **Multi-format Generation** — Select multiple output types and generate all from a single source
- **Flexible Input** — Paste text directly or upload files (TXT, PDF, DOCX, Markdown)
- **Configurable Parameters** — Control audience, tone, language, detail level, objective, style, temperature, and more
- **Download Outputs** — Export individual or combined results as Markdown files
- **Lightweight Model** — TinyLlama (~2GB) runs on CPU or GPU with minimal resources

## Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.9 or higher |
| RAM | 4 GB minimum (8 GB recommended) |
| Disk | 5 GB free (for model + dependencies) |
| OS | macOS, Linux, or Windows (WSL2) |

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/GenAi_Based_content_Transformer.git
cd GenAi_Based_content_Transformer
```

### 2. Run Setup Script (Recommended)

```bash
chmod +x setup.sh
./setup.sh
```

This creates a virtual environment, installs all dependencies, and configures Streamlit.

### 3. Manual Setup (Alternative)

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows (WSL2)

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Launch the Application

```bash
streamlit run app.py
```

The dashboard opens at **http://localhost:8501**. On first run, TinyLlama (~2GB) downloads automatically and is cached locally for future offline use.

## Usage

### Input Content
- **Text Input** — Type or paste source content directly
- **File Upload** — Upload `.txt`, `.pdf`, `.docx`, or `.md` files

### Select Output Types
Check one or more output formats:

| Output Type | What It Generates |
|---|---|
| **Video** | Script, storyboard, scene descriptions, narration, subtitles, visual recommendations |
| **LinkedIn Post** | Professional post with hook, body, hashtags, ready to publish |
| **Twitter/X Post** | Single tweet + tweet thread + engagement tweet |
| **Advisory** | Structured advisory with findings, risks, recommendations |
| **Infographic** | Content sections, layout recommendations, key messaging |
| **Executive Summary** | Concise briefing with key points, recommendations, next steps |
| **Presentation** | Slide-by-slide content with speaker notes and design tips |

### Configure Parameters
Adjust generation parameters in the sidebar and main panel:
- **Max Output Tokens** — Controls output length (256–2048)
- **Temperature** — Creativity level (0.1 = focused, 1.5 = creative)
- **Top-P** — Nucleus sampling threshold
- **Target Audience** — Who the content is for
- **Tone** — Professional, casual, formal, persuasive, etc.
- **Language** — Output language (default: English)
- **Level of Detail** — Very concise to very detailed
- **Communication Objective** — The goal of the content
- **Content Style** — Blog, academic, marketing, etc.

### Generate & Download
Click **Generate Content**, review outputs in tabs, and download individual files or all outputs combined as Markdown.

## Project Structure

```
GenAi_Based_content_Transformer/
├── app.py                  # Streamlit dashboard (main entry point)
├── model_loader.py         # TinyLlama model loading and inference
├── prompt_templates.py     # Engineered prompts for each output type
├── output_generators.py    # Generation orchestration logic
├── requirements.txt        # Python dependencies
├── setup.sh                # Automated setup script
├── .streamlit/
│   └── config.toml         # Streamlit theme configuration
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web-based dashboard UI |
| `torch` | PyTorch for model inference |
| `transformers` | Hugging Face model loading |
| `accelerate` | Device mapping and optimization |
| `sentencepiece` | Tokenizer backend |
| `PyPDF2` | PDF file reading |
| `python-docx` | DOCX file reading |
| `Pillow` | Image processing support |
| `plotly` | Charting support |
| `markdown` | Markdown rendering |

## Model Details

| Property | Value |
|---|---|
| Model | `TinyLlama/TinyLlama-1.1B-Chat-v1.0` |
| Parameters | ~1.1 Billion |
| Architecture | LLaMA 2 based |
| Precision | FP16 (GPU) / FP32 (CPU on macOS) |
| Context Window | 2048 tokens |
| License | Apache 2.0 |

The model is downloaded from Hugging Face on first run and cached in `~/.cache/huggingface/`.

## Platform Notes

| Platform | Device | Precision | Notes |
|---|---|---|---|
| Linux (NVIDIA GPU) | GPU (CUDA) | FP16 | Fastest. Automatic GPU detection. |
| macOS (Apple Silicon) | CPU | FP32 | MPS not supported for TinyLlama. Runs on CPU — slower but stable. |
| macOS (Intel) | CPU | FP32 | Runs on CPU. |
| Windows (WSL2 + NVIDIA) | GPU (CUDA) | FP16 | Requires WSL2 with CUDA support. |

## Troubleshooting

**Model download fails:**
Ensure you have internet for the first run. After download, the model works fully offline.

**`Placeholder storage has not been allocated on MPS device` (macOS):**
The app automatically avoids MPS and runs on CPU. If you still see this error, clear the model cache and restart:
```bash
rm -rf ~/.cache/huggingface/hub/models--TinyLlama--TinyLlama-1.1B-Chat-v1.0
streamlit run app.py
```

**Out of memory:**
- Reduce `Max Output Tokens` in the sidebar
- Close other applications to free RAM
- The model uses ~2GB RAM on CPU, ~4GB on GPU

**Slow generation:**
- Reduce `Max Output Tokens` for faster results
- Lower `Temperature` for more deterministic output
- On macOS, generation is slower on CPU — this is expected. Use shorter source content for faster results.
- On Linux with NVIDIA GPU, generation is significantly faster.

**Empty or poor-quality output:**
- Try shorter source content (the context window is 2048 tokens total)
- Select fewer output types at once (generate one at a time for best results)
- Adjust `Temperature` (lower = more focused, e.g., 0.5)

**Import errors:**
```bash
pip install -r requirements.txt
```

**Streamlit port already in use:**
```bash
streamlit run app.py --server.port 8502
```

## License

This project uses the TinyLlama model which is licensed under [Apache 2.0](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0/blob/main/LICENSE).
