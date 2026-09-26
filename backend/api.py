"""
FastAPI backend for the Gen AI Content Transformer.

Serves the JSON API for generation and (when built) the React frontend.
Run with: uvicorn backend.api:app --host 0.0.0.0 --port 8000
"""

import os
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .output_generators import generate_output
from .model_service import get_model_info, load_model, unload_model
from .prompt_templates import PROMPT_BUILDERS

app = FastAPI(title="Gen AI Content Transformer API", version="1.0.0")

# CORS for React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static frontend (built files). Frontend build outputs to ../frontend/dist
FRONTEND_DIST = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "frontend", "dist",
)


class GenerateRequest(BaseModel):
    output_type: str
    source_content: str
    audience: str = "general professional audience"
    tone: str = "Professional"
    language: str = "English"
    detail_level: str = "Moderate"
    objective: str = "inform and engage"
    style: str = "professional"
    max_new_tokens: int = Field(default=1024, ge=64, le=2048)
    temperature: float = Field(default=0.7, ge=0.1, le=1.5)
    top_p: float = Field(default=0.9, ge=0.1, le=1.0)


@app.get("/api/health")
def health():
    try:
        load_model()
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    return {"status": "ok"}


@app.get("/api/model-info")
def model_info():
    return get_model_info()


@app.get("/api/output-types")
def output_types():
    return {"output_types": list(PROMPT_BUILDERS.keys())}


@app.post("/api/generate")
def api_generate(request: GenerateRequest):
    return generate_output(
        output_type=request.output_type,
        source_content=request.source_content,
        audience=request.audience,
        tone=request.tone,
        language=request.language,
        detail_level=request.detail_level,
        objective=request.objective,
        style=request.style,
        max_new_tokens=request.max_new_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
    )


@app.post("/api/unload-model")
def api_unload_model():
    unload_model()
    return {"status": "ok", "detail": "Model unloaded from memory."}


# ── Serve the built React frontend ────────────────────────────────────────────
if os.path.isdir(FRONTEND_DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="static")

    @app.get("/")
    def serve_frontend():
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        candidate = os.path.join(FRONTEND_DIST, full_path)
        if os.path.isfile(candidate):
            return FileResponse(candidate)
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))