#!/bin/bash

# 运行模型分析
echo "Running model analysis..."
python src/model.py

# 生成图表
echo "Generating charts..."
python src/plotter.py

echo "Analysis completed successfully!"
echo "Results are available in the 'results' directory."
