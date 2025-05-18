# Market Cap Weighted Index CLI

A command-line tool for constructing and rebalancing a market capitalization-weighted index.

## Assessment Context
This project was developed as part of a job application technical assessment for a software engineering role.

## Overview

This tool implements a market cap-weighted index fund model that:
- Constructs an index based on market capitalization data
- Allocates funds according to market cap weights
- Rebalances the portfolio on multiple dates
- Maintains exposure to companies within a specified cumulative weight threshold

## Prerequisites
- Python 3.12 or newer
- pip

## Installation
### Clone the Repository
```sh
git clone https://github.com/lukestagoll/cap-weighted-index-cli.git
cd cap-weighted-index-cli
```

### Create a Virtual Environment
```sh
python -m venv .venv
```

### Activate the Virtual Environment
#### Linux/macOS
```sh
source .venv/bin/activate
```

#### Windows (Powershell)
```sh
.\.venv\Scripts\Activate.ps1
```

### Install Dependencies
#### For Development Usage
Install in editable mode:
```sh
pip install -e .
```

#### For Standard Usage
Install:
```sh
pip install .
```

## Usage
The application can be run using `cap-weighted-index` or `cwi`.

Run with default values:
```sh
cwi
```

Display help for the main command:
```sh
cwi --help
```

Command Options
- `--input, -i`: Path to input CSV file (default: data/input/market_capitalisation.csv)
- `--available-funds`: Initial funds available for investment (default: 100,000,000.00)
- `--max-cumulative-weight`: Maximum cumulative weight threshold (default: 0.85)

### Input Data Format
The tool expects a CSV file with the following columns:

- `date`: Date in format DD/MM/YYYY
- `company`: Company identifier
- `market_cap_m`: Market capitalization in millions
- `price`: Share price

## How It Works
1. The tool loads market data from CSV
2. For each date:
    - Sorts companies by market cap
    - Calculates weights and cumulative weights
    - Includes companies up to the specified cumulative weight threshold
    - Sells companies that fell below the threshold
    - Buys companies that rose above the threshold
    - Provides detailed portfolio reporting

## Project Structure
- `cap_weighted_index_cli` - Main package
  - `analysis/` - Weight calculation modules
  - `data` - CSV parsing and data validation
  - `execution/` - Trade execution logic
  - `logging/` - Portfolio and transaction reporting
  - `market/` - Market data processing
  - `models/` - Data models
  - `portfolio/` - Portfolio management

## Running Tests
Use Python’s built-in unittest discovery:
```sh
python -m unittest discover
```
## Known Issues
See docs/issues.md for a discussion of limitations and potential improvements.

## Original plan
See docs/plan.md for my original plan - the final product has deviated.

## License
Distributed under the MIT License. See the LICENSE file for details.