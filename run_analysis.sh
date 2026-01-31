#!/bin/bash

# 运行模型分析
echo "Running model analysis..."
python -m src.model

# 生成图表
echo "Generating charts..."
python -m src.plotter

echo "Analysis completed successfully!"
echo "Results are available in the 'results' directory."
