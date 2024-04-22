# Data collection

Follow these steps to start the data collection process:

1. Make sure you have Node.js installed

   ```sh
    node --version # tested with version 18.14.0
   ```

1. Go to the collection folder

   ```sh
    cd collection
   ```

1. Install pnpm package manager

   ```sh
    npm install -g pnpm
   ```

1. Install project dependencies

   ```sh
    pnpm install
   ```

1. Find stations and save them to `hafas.db`

   ```sh
    node stations.js
   ```

1. Start to monitor departures

   ```sh
   node monitor.js
   ```

1. After stopping the monitor script, convert departures and stations tables into CSV files
   ```sh
   sqlite3 -header -csv hafas.db 'select * from departures;' > departures.csv
   sqlite3 -header -csv hafas.db 'select * from stations;' > stations.csv
   ```
