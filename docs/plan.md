# Market Cap Weighted Index Fund
This project implements a market cap-weighted index fund model using Python. It constructs an index and performs periodic rebalancing based on financial data from an input CSV file.

## Task
### Input
- Provided with a CSV file containing:
  - Date - "date"
  - Company - "company"
  - Market Cap - "market_cap_m"
  - Price - "price"

### Index Construction
1. **Load & Filter** the data for `2025-04-08`
2. **Sort** by descending market cap.
3. **Compute total market cap**
4. **Calculate** company:
   - Weight = Company Market Cap / Total Market Cap
   - Cumulative Weight
5. **Filter up to 85% Cumulative Weight**
6. **Allocate $100M**
   - shares = $100M * weight / price

### Rebalancing
1. Filter the data for the second date (`2025-05-08`).
2. Repeat steps 2–4 from the Index Construction section on this new data set.
3. Determine a new fund universe, i.e., which stocks make the cutoff (85th percentile) on the new market caps.
   - If a stock was not in the original list BUT is in the new universe, it will be bought.
   - If a stock is in the original list BUT not in the new universe, it will be sold from the fund.
4. Calculate:
   - The value of your portfolio at the second date
   - The quantity of any new equities purchased by the fund.
   - Identify which equity(ies) are being sold and their total value.

### Requirements
- Use clear naming and folder structure.
- Code should be well-structured and commented.
- Include a `README.md` with setup and run instructions.
- (Optional) Include unit tests.

### Scenarios & Real World Considerations
- In a commented section, list and describe in the script as many scenarios as you can where:
  - The data is incorrect (e.g., formatting, content).
  - The code might break.
- Write the necessary requirements to be able to identify your sources of error.
- Using your knowledge & research of market weighted index funds, list and describe what may be missing from this dataset & hence the code.

---

<br>

## Dependencies
I have chosen to utilise [numpy](#numpy) and [pandas](#pandas) in this project.

Without the use of these external dependencies I would need to:
    - manually parse CSV files
    - write logic for caculating weights & cumulative sums
    - manage data with lists & dictionaries

Pandas and numpy are an industry standard which means the code will be easier for others to read, trust, and build on.

### `numpy`
- Uses contiguous arrays rather than vanilla python lists - efficient data processing since elements are stored in adjacent memory locations
- Contiguous arrays allows for vectorised operations - no looping for calculations
- Provides a cumulative sum function which is faster than manual calculations with vanilla python lists & loops.

### `pandas`
- Purpose built for tabular data - CSV
- Intuitive filtering, sorting & grouping operations
- Minimal overhead - gaining clarity & maintailability without sacrificing speed


## Example

### Input (CSV)
```csv
date,company,market_cap_m,price
8/04/2025,A,1200,12.32
8/04/2025,B,800,4.52
8/04/2025,C,4000,8.45
8/04/2025,D,1200,1.99
8/04/2025,E,900,13.43
8/04/2025,F,600,19.45
8/04/2025,G,800,2.31
8/04/2025,H,150,0.88
8/05/2025,A,1300,13.35
8/05/2025,B,750,4.24
8/05/2025,C,3000,6.34
8/05/2025,D,200,0.33
8/05/2025,E,1000,14.92
8/05/2025,F,700,22.69
8/05/2025,G,500,1.44
8/05/2025,H,900,5.28
```

### Read CSV with pandas
```py
market_data = pd.read_csv("market_capitalisation.csv", parse_dates=["date"], dayfirst=True)
```

#### market_data
```
| date      | company | market_cap_m | price |
|-----------|---------|--------------|-------|
| 8/04/2025 | A       | 1200         | 12.32 |
| 8/04/2025 | B       | 800          | 4.52  |
| 8/04/2025 | C       | 4000         | 8.45  |
| 8/04/2025 | D       | 1200         | 1.99  |
| 8/04/2025 | E       | 900          | 13.43 |
| 8/04/2025 | F       | 600          | 19.45 |
| 8/04/2025 | G       | 800          | 2.31  |
| 8/04/2025 | H       | 150          | 0.88  |
| 8/05/2025 | A       | 1300         | 13.35 |
| 8/05/2025 | B       | 750          | 4.24  |
| 8/05/2025 | C       | 3000         | 6.34  |
| 8/05/2025 | D       | 200          | 0.33  |
| 8/05/2025 | E       | 1000         | 14.92 |
| 8/05/2025 | F       | 700          | 22.69 |
| 8/05/2025 | G       | 500          | 1.44  |
| 8/05/2025 | H       | 900          | 5.28  |
```

### Extract Dates
extract a list of dates to perform calculations on - avoids hardcoding the number of calculations to perform - ensures extensibility.
```py
# { "8/04/2025", "8/05/2025" }
dates = market_data["date"].drop_duplicates().sort_values()
```

### Construct Index
#### Filter Data for the Earliest Date
```py
# | date      | company | market_cap_m | price |
# |-----------|---------|--------------|-------|
# | 8/04/2025 | A       | 1200         | 12.32 |
# | 8/04/2025 | B       | 800          | 4.52  |
# | 8/04/2025 | C       | 4000         | 8.45  |
# | 8/04/2025 | D       | 1200         | 1.99  |
# | 8/04/2025 | E       | 900          | 13.43 |
# | 8/04/2025 | F       | 600          | 19.45 |
# | 8/04/2025 | G       | 800          | 2.31  |
# | 8/04/2025 | H       | 150          | 0.88  |

market_snapshot = market_data[market_data["date"] == dates[0]]
```

#### Sort by Descending Market Cap
```py
# | date      | company | market_cap_m | price |
# |-----------|---------|--------------|-------|
# | 8/04/2025 | C       | 4000         | 8.45  |
# | 8/04/2025 | A       | 1200         | 12.32 |
# | 8/04/2025 | D       | 1200         | 1.99  |
# | 8/04/2025 | E       | 900          | 13.43 |
# | 8/04/2025 | B       | 800          | 4.52  |
# | 8/04/2025 | G       | 800          | 2.31  |
# | 8/04/2025 | F       | 600          | 19.45 |
# | 8/04/2025 | H       | 150          | 0.88  |

market_snapshot = market_snapshot.sort_values("market_cap_m", ascending=False)
```

#### Calculate Total Market Cap
```py
total_market_cap = market_snapshot["market_cap_m"].sum()
```

#### Calculate Weight
```py
# | date      | company | market_cap_m | price | weight |
# |-----------|---------|--------------|-------|--------|
# | 8/04/2025 | C       | 4000         | 8.45  | 0.4145 |
# | 8/04/2025 | A       | 1200         | 12.32 | 0.1243 |
# | 8/04/2025 | D       | 1200         | 1.99  | 0.1243 |
# | 8/04/2025 | E       | 900          | 13.43 | 0.0932 |
# | 8/04/2025 | B       | 800          | 4.52  | 0.0829 |
# | 8/04/2025 | G       | 800          | 2.31  | 0.0829 |
# | 8/04/2025 | F       | 600          | 19.45 | 0.0621 |
# | 8/04/2025 | H       | 150          | 0.88  | 0.0155 |

market_snapshot["weight"] = market_snapshot["market_cap_m"] / total_market_cap
```

#### Calculate Cumulative Weight
```py
# | date      | company | market_cap_m | price | weight | cumulative_weight |
# |-----------|---------|--------------|-------|--------|-------------------|
# | 8/04/2025 | C       | 4000         | 8.45  | 0.4145 | 0.4145            |
# | 8/04/2025 | A       | 1200         | 12.32 | 0.1243 | 0.5388            |
# | 8/04/2025 | D       | 1200         | 1.99  | 0.1243 | 0.6632            |
# | 8/04/2025 | E       | 900          | 13.43 | 0.0932 | 0.7564            |
# | 8/04/2025 | B       | 800          | 4.52  | 0.0829 | 0.8393            |
# | 8/04/2025 | G       | 800          | 2.31  | 0.0829 | 0.9222            |
# | 8/04/2025 | F       | 600          | 19.45 | 0.0621 | 0.9844            |
# | 8/04/2025 | H       | 150          | 0.88  | 0.0155 | 0.9999            |

market_snapshot["cumulative_weight"] = market_snapshot["weight"].cumsum()
```

#### Filter up to 85%
```py
# | date      | company | market_cap_m | price | weight | cumulative_weight |
# |-----------|---------|--------------|-------|--------|-------------------|
# | 8/04/2025 | C       | 4000         | 8.45  | 0.4145 | 0.4145            |
# | 8/04/2025 | A       | 1200         | 12.32 | 0.1243 | 0.5388            |
# | 8/04/2025 | D       | 1200         | 1.99  | 0.1243 | 0.6632            |
# | 8/04/2025 | E       | 900          | 13.43 | 0.0932 | 0.7564            |
# | 8/04/2025 | B       | 800          | 4.52  | 0.0829 | 0.8393            |

current_portfolio = market_snapshot[market_snapshot["cumulative_weight"] <= np.float64(0.85)]
```

#### Calculate Shares to Buy

```py
# | date      | company | market_cap_m | price | weight | cumulative_weight | shares  |
# |-----------|---------|--------------|-------|--------|-------------------|---------|
# | 8/04/2025 | C       | 4000         | 8.45  | 0.4145 | 0.4145            | 4905417 |
# | 8/04/2025 | A       | 1200         | 12.32 | 0.1243 | 0.5388            | 1009353 |
# | 8/04/2025 | D       | 1200         | 1.99  | 0.1243 | 0.6632            | 6248860 |
# | 8/04/2025 | E       | 900          | 13.43 | 0.0932 | 0.7564            | 694447  |
# | 8/04/2025 | B       | 800          | 4.52  | 0.0829 | 0.8393            | 1834105 |

available_funds = 100000000
current_portfolio["shares"] = np.floor(available_funds * current_portfolio["weight"] / current_portfolio["price"])
```

#### Allocate Funds
```py
# | date      | company | market_cap_m | price | weight | cumulative_weight | shares  | value       |
# |-----------|---------|--------------|-------|--------|-------------------|---------|-------------|
# | 8/04/2025 | C       | 4000         | 8.45  | 0.4145 | 0.4145            | 4905417 | 41450773.65 |
# | 8/04/2025 | A       | 1200         | 12.32 | 0.1243 | 0.5388            | 1009353 | 12435228.96 |
# | 8/04/2025 | D       | 1200         | 1.99  | 0.1243 | 0.6632            | 6248860 | 12435231.40 |
# | 8/04/2025 | E       | 900          | 13.43 | 0.0932 | 0.7564            | 694447  | 9326423.21  |
# | 8/04/2025 | B       | 800          | 4.52  | 0.0829 | 0.8393            | 1834105 | 8290154.60  |

current_portfolio["value"] = current_portfolio["shares"] * current_portfolio["price"]
```

#### Calculate Funds Remaining

```py
# funds_remaining = 100000000 - 83937034.42 = 16062965.58
funds_remaining = available_funds - current_portfolio["value"].sum()
available_funds = funds_remaining
```

### Rebalance Index
Loop over subsequent dates:
```py
for date in unique_dates.iloc[1:]:
    # construct market_snapshot
    # sort by descending market cap
    # calc total market cap
    # calc weight
    # calc cumulative weight
    # filter up to 85%
    # compare companies in current_portfolio & new market_snapshop
    # Sell stocks
    # buy stocks
    # recalculate portfolio value
```

#### Get the next Market Snapshot & Filter up to the 85th Percentile
```py
# | date      | company | market_cap_m | price | weight | cumulative_weight |
# |-----------|---------|--------------|-------|--------|-------------------|
# | 8/05/2025 | C       | 3000         | 6.34  | 0.3592 | 0.3592            |
# | 8/05/2025 | A       | 1300         | 13.35 | 0.1556 | 0.5149            |
# | 8/05/2025 | E       | 1000         | 14.92 | 0.1197 | 0.6347            |
# | 8/05/2025 | H       | 900          | 5.28  | 0.1077 | 0.7425            |
# | 8/05/2025 | B       | 750          | 4.24  | 0.0898 | 0.8323            |
```

#### Compare Companies in Portfolio with New Market Snapshot
```py
# companies_invested = { "A", "C", "D", "E", "B" }
# companies_to_invest = { "A", "H", "C", "E", "B" }
companies_invested = set(current_portfolio["company"])
companies_to_invest = set(market_snapshot["company"])


# sell_stocks = { "D" }
# buy_stocks = { "H" }
sell_stocks = companies_invested - companies_to_invest
buy_stocks = companies_to_invest - companies_invested
```

#### Sell Stocks
```py
# | date      | company | market_cap_m | price | weight | cumulative_weight | shares  | value      | 
# |-----------|---------|--------------|-------|--------|-------------------|---------|------------|
# | 8/05/2025 | D       | 200          | 0.33  | 0.0239 | 0.9999            | 6248860 | 2062123.80 |

to_sell = current_portfolio[current_portfolio["company"].isin(sell_stocks)]
to_sell = to_sell.merge(
    market_snapshot[["company", "price"]],
    on="company",
    how="left"
)
to_sell["value"] = to_sell["shares"] * to_sell["price"]

# available_funds = 18125089.38
available_funds += to_sell["value"].sum()
```

#### Remove Sold Stocks from Portfolio
```py
# | date      | company | market_cap_m | price | weight | cumulative_weight | shares  | value       |
# |-----------|---------|--------------|-------|--------|-------------------|---------|-------------|
# | 8/04/2025 | C       | 3000         | 6.34  | 0.3592 | 0.3592            | 4905417 | 31100343.78 |
# | 8/04/2025 | A       | 1300         | 13.35 | 0.1556 | 0.5149            | 1009353 | 13474862.55 |
# | 8/04/2025 | E       | 1000         | 14.92 | 0.1197 | 0.6347            | 694447  | 10361149.24 |
# | 8/04/2025 | B       | 750          | 4.24  | 0.0898 | 0.8323            | 1834105 | 7776605.20  |

current_portfolio = current_portfolio[~current_portfolio["company"].isin(sell_stocks)]
```

#### Buy Stocks
```py
# | date      | company | market_cap_m | price | weight | cumulative_weight | shares  | value      | 
# |-----------|---------|--------------|-------|--------|-------------------|---------|------------|
# | 8/05/2025 | H       | 900          | 5.28  | 0.1077 | 0.7425            | 369710  | 1952068.80 |
to_buy = market_snapshot[market_snapshot["company"].isin(buy_stocks)]
to_buy = to_buy.merge(
    market_snapshot[["company", "price"]],
    on="company",
    how="left"
)
to_buy["shares"] = np.floor(available_funds * to_buy["weight"] / to_buy["price"])
to_buy["value"] = to_buy["shares"] * to_buy["price"]

# available_funds = 16173020.58
available_funds -= to_buy["value"].sum()
```

#### Add Bought Stocks to Portfolio
```py
# | date      | company | market_cap_m | price | weight | cumulative_weight | shares  | value       |
# |-----------|---------|--------------|-------|--------|-------------------|---------|-------------|
# | 8/04/2025 | C       | 3000         | 6.34  | 0.3592 | 0.3592            | 4905417 | 31100343.78 |
# | 8/04/2025 | A       | 1300         | 13.35 | 0.1556 | 0.5149            | 1009353 | 13474862.55 |
# | 8/04/2025 | E       | 1000         | 14.92 | 0.1197 | 0.6347            | 694447  | 10361149.24 |
# | 8/04/2025 | H       | 900          | 5.28  | 0.1077 | 0.7425            | 369710  | 1952068.80  |
# | 8/04/2025 | B       | 750          | 4.24  | 0.0898 | 0.8323            | 1834105 | 7776605.20  |

current_portfolio = pd.concat([current_portfolio, to_buy], ignore_index=True).sort_values(by="market_cap_m").reset_index(drop=True)
```

<br>

## Planned Structure

```py
index_rebalance/
├── docs/                           # project docs
|   ├── architecture.md             # project architecture & design choices
|   ├── usage.md                    # usage docs
|   └── api/                        # api doc
|       ├── company.py
|       └── portfolio.py
├── src/
|   └──cap_weighted_index_cli/
|       ├── models/                 # data classes
|       |   ├── company.py
|       |   ├── market.py
|       |   └── portfolio.py
|       ├── utils/
|       |   ├── logging.py          # logging utils
|       |   ├── config.py           # config management [future improvement]
|       |   └── validation.py       # data validation
|       ├── data/
|       |   ├── parse_csv.py        # parse input csv file
|       |   ├── market_cap.py       # market cap parsing functions
|       |   └── market_totals.py    # total market calculations
|       ├── analysis/
|       |   ├── weights.py          # weight calculations
|       |   ├── filters.py          # company filtering logic
|       |   └── sorting.py          # sorting algorithms
|       ├── portfolio/
|       |   ├── valuation.py        # portfolio valuation
|       |   ├── allocation.py       # share allocation calculations
|       |   └── transactions.py     # entry & exit logic
|       ├── execution/
|       |   ├── trade.py            # trade execution
|       |   └── rebalance.py        # rebalace coordination
|       └── cli.py                  # entry point
├── tests/                          # same structure as /src, filenames prefixed with "test_"
├── data/                           # input/output data dir
|   ├── input/
|   └── output/
├── config/                         # config files
|   └── config.yaml
├── requirements.txt                # project dependencies
├── setup.py                        # package installation
└── README.md                       # main docs
```
