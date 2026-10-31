#!/usr/bin/env bash
# ==============================================================================
# Deploy Clinical Web App to Hugging Face Spaces (spatial-continuum-lab/spatial-continuum-clinical-app)
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HF_REPO_DIR="/home/luca/spatial-continuum-clinical-app"

echo "🚀 Deploying Clinical Decision Web App to Hugging Face Spaces..."

if [ ! -d "$HF_REPO_DIR/.git" ]; then
    echo "❌ Error: Hugging Face repository directory not found at $HF_REPO_DIR"
    exit 1
fi

# Copy latest files from main repository into Hugging Face local clone
cp "$SCRIPT_DIR/index.html" "$HF_REPO_DIR/index.html"
cp "$SCRIPT_DIR/style.css" "$HF_REPO_DIR/style.css"
cp "$SCRIPT_DIR/README.md" "$HF_REPO_DIR/README.md"

cd "$HF_REPO_DIR"

if git diff --quiet && git diff --staged --quiet; then
    echo "✅ No changes to deploy. Hugging Face Space is already up to date!"
else
    git add index.html style.css README.md
    COMMIT_MSG="deploy: sync clinical web app from main repo ($(date +'%Y-%m-%d %H:%M:%S'))"
    git commit -m "$COMMIT_MSG"
    echo "📡 Pushing updates to Hugging Face Spaces remote..."
    git push origin main
    echo "🎉 Successfully deployed to: https://huggingface.co/spaces/spatial-continuum-lab/spatial-continuum-clinical-app"
fi
