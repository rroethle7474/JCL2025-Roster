# JCL Fantasy Baseball Salary Processor

This Python application processes fantasy baseball player data for the JCL (likely "John's/Jane's/Your Custom League") to prepare salary information for the 2025 season.

## Overview

The application performs the following tasks:
1. Reads player data from three CSV files:
   - `2024-JCL-Player-List.csv`: Contains current player information including 2024 salaries
   - `2025-JCL-Import.csv`: Base import file for the 2025 season
   - `2025-JCL-Keeper-Eligible-List.csv`: List of players eligible to be kept for 2025 with their keeper salaries

2. Processes the data by:
   - Cleaning salary data (removing currency symbols, converting to numeric)
   - Matching players across files using PlayerIds
   - Validating 2024 salaries between files
   - Identifying unmatched players
   - Updating the 2025 import file with keeper salaries

3. Outputs a final CSV file:
   - `2025-JCL-Import-Final.csv`: The processed import file with updated 2025 salaries

## Requirements

- Python 3.6+
- pandas
- numpy

## Installation

1. Clone this repository or download the files
2. Install the required packages:

```bash
pip install pandas numpy
```

## Usage

1. Ensure your three input CSV files are in the same directory as the script:
   - `2024-JCL-Player-List.csv`
   - `2025-JCL-Import.csv`
   - `2025-JCL-Keeper-Eligible-List.csv`

2. Run the script:

```bash
python app.py
```

3. The script will:
   - Log its progress to the console
   - Report any salary mismatches or unmatched players
   - Create the output file `2025-JCL-Import-Final.csv`

## Using the Script for Future Years (2026+)

To use this script for future seasons, you'll need to:

1. Update the file names in the script:
   - Open `app.py` in a text editor
   - Locate the file reading section (around line 10-12)
   - Update the year in each filename to match the target year
   - Example for 2026:
     ```python
     players_2025 = pd.read_csv('2025-JCL-Player-List.csv')
     import_2026 = pd.read_csv('2026-JCL-Import.csv')
     keepers_2026 = pd.read_csv('2026-JCL-Keeper-Eligible-List.csv')
     ```

2. Update the column references:
   - Change `2024_Salary` to the appropriate year (e.g., `2025_Salary`)
   - Change `24_Salary` and `25_Salary` to the appropriate years (e.g., `25_Salary` and `26_Salary`)
   - Update the output file name (e.g., `2026-JCL-Import-Final.csv`)

3. Prepare your input files with the updated naming convention:
   - Previous year's player list (e.g., `2025-JCL-Player-List.csv`)
   - Current year's import file (e.g., `2026-JCL-Import.csv`)
   - Current year's keeper list (e.g., `2026-JCL-Keeper-Eligible-List.csv`)

4. Run the script as usual:
   ```bash
   python app.py
   ```

Alternatively, you could modify the script to accept command-line arguments for the years, making it more flexible without requiring code changes each season.

## Input File Requirements

### 2024-JCL-Player-List.csv
- Must contain columns: `Player`, `PlayerId`, `2024_Salary`

### 2025-JCL-Import.csv
- Must contain column: `PlayerId`

### 2025-JCL-Keeper-Eligible-List.csv
- Must contain columns: `Player`, `Team`, `24_Salary`, `25_Salary`

## Output

The final output file `2025-JCL-Import-Final.csv` will contain all players from the import file with updated 2025 salaries for keeper-eligible players.

## Troubleshooting

The application includes detailed logging to help identify issues:
- Salary mismatches between the 2024 player list and keeper list
- Players in the keeper list that couldn't be matched to the 2024 player list
- Statistics about how many players were updated

If you encounter any issues, check the console output for error messages and warnings.
