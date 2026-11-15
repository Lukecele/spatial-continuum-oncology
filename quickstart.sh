#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

echo ""
echo "=========================================================================="
echo -e "\033[1;33m ⭐ Support Open Science: Please Star the Repository on GitHub!\033[0m"
echo -e "\033[4;34m 👉 https://github.com/Lukecele/spatial-continuum-oncology\033[0m"
echo "=========================================================================="
echo ""
echo "🔬 Launching Spatial Continuum Reaction-Diffusion CRI Calculator..."
echo ""

python3 "$DIR/src/spatial_continuum/cri_calc.py" "$@"
