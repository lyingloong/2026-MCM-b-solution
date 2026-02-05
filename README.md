# [2026 MCM Problem B: Creating a Moon Colony Using a Space Elevator System](https://www.contest.comap.com/undergraduate/contests/mcm/contests/2026/problems/2026_MCM_Problem_B.pdf)

## Team Information
**Team Control Number**: 2622082

### Core Members
| Name | GitHub Profile |
| --- | --- |
| Hao Wang | [lyingloong](https://github.com/lyingloong) |
| Renhao Li | [LiRenHao](https://github.com/stdlibstring) |
| Wenchao Yu | [ANT181603](https://github.com/ANT181603) |

## Project Overview
This repository contains the solution for the 2026 MCM Problem B, which focuses on creating a moon colony using a space elevator system. The analysis includes three scenarios: using only space elevators, using only traditional rockets, and a combined approach with optimal ratio. The solution also includes detailed analysis for three different problem formulations, with Problem 3 analyzed at monthly granularity.

## Repository Structure
- `data/`: Contains data files used in the analysis
  - `Global_Space_Exploration_Dataset.csv`: Original dataset from Kaggle (https://www.kaggle.com/datasets/atharvasoundankar/global-space-exploration-dataset-2000-2025)
  - `space_launch_data_2000_2025.csv`: Processed data based on the original dataset
- `results/`: Contains output results and visualizations
- `figures/`: Generated figures for the analysis
- `src/`: Main source code
  - `main_model.py`: Core model implementation for scenario analysis
  - `constants.py`: Constants used in the model
  - `plotter.py`: Chart generation for visualizing results
  - `sensitivity_analysis_v1.py`: Basic sensitivity analysis for model parameters
  - `sensitivity_analysis_v2.py`: Enhanced sensitivity analysis with smooth visualization
  - `pollution_analysis.py`: Pollution analysis
- `run_main.sh`: Bash script to run the complete analysis
- `requirements.txt`: Dependencies required for the project
- `README.md`: Project documentation

## Getting Started
1. Clone this repository
2. Install necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the analysis script:
   ```bash
   bash run_main.sh
   ```

## Dependencies
- Python 3.8+
- numpy
- matplotlib
- scipy

## License
MIT License
