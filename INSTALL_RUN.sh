#!/usr/bin/env bash
set -e
echo "Setting up project scaffold (backend + frontend)"

# Backend
cd backend
python3 -m venv .venv || true
source .venv/bin/activate
pip install -r requirements.txt

echo "Backend deps installed."

# Frontend
cd ../frontend
if [ -f package.json ]; then
  if command -v npm >/dev/null 2>&1; then
    npm ci --silent || npm install --silent
    npm run build --silent || true
  fi
fi

echo "Build step completed. Start backend with:"
echo "cd backend && source .venv/bin/activate && uvicorn main:app --reload --port 8000"
