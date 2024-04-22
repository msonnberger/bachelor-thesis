# Data analysis and visualization

Follow these steps to output all tables and visualizations shown in this thesis. The Python scripts require `departures.csv` and `stations.csv` to be located inside the `collection` directory.

1. Make sure you have Python installed

   ```sh
   python --version # tested with version 3.10.10
   ```

1. Go to the analysis folder

   ```sh
   cd analysis
   ```

1. Run analysis script to output tables and box plots (this may take a while!):

   ```sh
   python analysis.py
   ```

1. Run `map.py` to generate and output maps (fig. 4-6). You need a Mapbox access token saved as `.mapbox_token`!

   ```sh
   python map.py
   ```

1. Run `time_of_day.py` to generate line graphs (fig. 7, 8)
   ```sh
   python time_of_day.py
   ```
