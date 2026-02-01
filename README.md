# 2026 MCM Problem B: Creating a Moon Colony Using a Space Elevator System

## Team Information
- [Hao Wang](https://github.com/lyingloong)
- [Renhao Li](https://github.com/LiRenHao)
- [Wenchao Yu](https://github.com/ANT181603)

## Project Overview
This repository contains the solution for the 2026 MCM Problem B, which focuses on creating a moon colony using a space elevator system. The analysis includes three scenarios: using only space elevators, using only traditional rockets, and a combined approach with optimal ratio.

## Repository Structure
- `data/`: Contains data files used in the analysis
  - `Global_Space_Exploration_Dataset.csv`: Original dataset from Kaggle (https://www.kaggle.com/datasets/atharvasoundankar/global-space-exploration-dataset-2000-2025)
  - `space_launch_data_2000_2025.csv`: Processed data based on the original dataset
- `models/`: Contains models and algorithms implementation
- `results/`: Contains output results and visualizations
- `figures/`: Generated figures for the analysis
- `src/`: Main source code
  - `main_model.py`: Core model implementation for scenario analysis
  - `constants.py`: Constants used in the model
  - `plotter.py`: Chart generation for visualizing results
  - `sensitivity_analysis.py`: Sensitivity analysis for model parameters(SE system)
- `run_analysis.sh`: Bash script to run the complete analysis
- `README.md`: Project documentation

## Getting Started
1. Clone this repository
2. Install necessary dependencies:
   ```bash
   pip install numpy matplotlib
   ```
3. Run the analysis script:
   ```bash
   bash run_analysis.sh
   ```

## Dependencies
- Python 3.8+
- numpy
- matplotlib

## License
MIT License
