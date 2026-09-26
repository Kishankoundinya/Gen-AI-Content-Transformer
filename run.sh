#!/bin/bash
# Gen AI Content Transformer - Run Script
# Usage:
#   ./run.sh          -> production mode (serves built React UI on :8000)
#   ./run.sh --dev    -> dev mode (backend :8000 + Vite dev server :5173)

set -e

PORT=8000

if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Run ./setup.sh first."
    exit 1
fi

# shellcheck disable=SC1091
source .venv/bin/activate

if [ "$1" = "--dev" ]; then
    echo "Starting backend on http://localhost:8000 ..."
    echo "Starting frontend dev server on http://localhost:5173 ..."
    (cd frontend && npm run dev) &
  uvicorn backend.api:app --host 0.0.0.0 --port "$PORT" --reload
else
    if [ ! -d "frontend/dist" ]; then
        echo "Frontend build not found. Run ./setup.sh to build the UI."
        exit 1
    fi
    echo "Starting Gen AI Content Transformer..."
    echo "Open http://localhost:8000 in your browser"
    uvicorn backend.api:app --host 0.0.0.0 --port "$PORT"
fi