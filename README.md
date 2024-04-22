# Bachelor Thesis

**Title:** _Detecting and Visualizing Delay Hotspots in Vienna's Public Transport Network_

## Folder structure

- `latex`: contains all LaTeX files, with the compiled PDF located in `latex/out`.
- `references`: contains all papers and websites downloaded as PDF. File names correspond to biblatex keys.
- `collection`: Node.js scripts for collecting departure data using the HAFAS API. See `README.md` inside for further instructions. This folder also includes the raw data used for analysis (`departures.csv` and `departures_small.csv` for a smaller version used for testing)
- `analysis`: Python scripts for analyzing and visualizing the collected data. See `README.md` inside for further instructions.
