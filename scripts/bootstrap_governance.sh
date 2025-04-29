#!/usr/bin/env bash
set -euo pipefail

echo "🔧  Installing Governance & Alignment bundle..."

# Install Python deps
pip install "dvc[azure]" great_expectations pennylane --quiet

# Initialise DVC if not present
if [ ! -d .dvc ]; then
  dvc init --quiet
fi

# Install pre‑commit hooks
if command -v pre-commit &>/dev/null; then
  pre-commit install
fi

echo "✅  Bundle installed. Commit and push to activate CI."
