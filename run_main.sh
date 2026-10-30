#!/usr/bin/env bash
#
# Reproduce every result in ./results from a clean checkout.
#
# Usage:
#   bash run_main.sh
#
# All figures and intermediate data are written to ./results, which is
# git-ignored on purpose: the figures committed under ./figures are the
# versions used in the paper.

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

# Headless plotting by default: plt.show() must not block CI or SSH sessions.
export MPLBACKEND="${MPLBACKEND:-Agg}"

echo "==> Main model (Problems 1-3)"
python -m src.main_model

echo "==> Core figures"
python -m src.plotter

echo "==> Problem 3: additional plots"
python -m src.p3_extra_plots

echo "==> Problem 2: reliability sensitivity analysis"
python -m src.p2_sensitivity_analysis

echo "==> Problem 4: environmental impact analysis"
python -m src.p4_pollution_analysis

echo "==> Problem 1: 3D sensitivity analysis"
python -m src.sensitivity_analysis_v2

echo
echo "Analysis completed successfully. Results are in ./results/"
