# Data

| File | Description |
| --- | --- |
| `Global_Space_Exploration_Dataset.csv` | Original dataset, downloaded from Kaggle: [Global Space Exploration Dataset (2000-2025)](https://www.kaggle.com/datasets/atharvasoundankar/global-space-exploration-dataset-2000-2025). |
| `space_launch_data_2000_2025.csv` | Processed extract derived from the file above. |

Notes:

- The model code does not read these CSVs at runtime; the calibrated values live
  in `src/constants.py`. The files are kept here for provenance and for readers
  who want to retrace the assumptions.
- The original Kaggle dataset is redistributed here under the terms attached to
  it on Kaggle. If you reuse it, cite the original author and check the current
  license on the dataset page.
