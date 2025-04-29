#!/usr/bin/env bash
set -euo pipefail

echo "🔧 Bootstrapping ATHENA project ..."

python -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r backend/requirements.txt

if command -v pre-commit &>/dev/null; then
  pre-commit install
fi

cd frontend
if [ -f package-lock.json ]; then
  npm ci
else
  npm install
fi
cd ..

echo "✅ Bootstrap complete. Use 'docker compose up --build' to start."
