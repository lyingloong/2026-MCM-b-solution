#!/bin/bash

# 运行模型分析
echo "Running model analysis..."
python -m src.main_model

# 生成图表
echo "Generating charts..."
python -m src.plotter

echo "Processing plots for Problem 3..."
cd results/problem_3
python extra_plot_generator_p3.py
cd -

echo "Analysis completed successfully!"
echo "Results are available in the 'results' directory."
