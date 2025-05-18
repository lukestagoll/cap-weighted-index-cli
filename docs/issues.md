# Issues with this approach
When rebalancing, the portfolio holds assets from the previous allocation. If the new weights are applied only to the available cash we end up underweighting the newly added stocks. This means our portfolio exposure is skewed and will deviate from the intended weight distribution.
This issue is exacerbated since we only sell stocks when a company is no longer within the 85% threshold and buy stocks when a company newly falls within the 85% threshold. As market caps change over time, our stock allocation doesn't follow suit, leading to more deviation over time, eventually not representing a valid market cap weighted index.

A solution to this issue is to rebalance the entire portfolio:
1. We calculate the value of the portfolio using current prices of all held shares and add available cash.
2. Calculate the target value of each stock to the current value
3. For each company:
   - if the current value is greater than the target value, sell a shares to meet the target value (this includes new companies since current value will be 0)
   - if the current value is less than the target value, buy shares to meet the target value.
   - if the current value equals the target value, do nothing.
   - if removed from the list, sell all.

There are trade-offs to this approach:
- Increased costs due to frequent transactions
  - Can be mitigated by introducing a threshold - only rebalance if weight deviates by `x`%
  - Can be mitigated by rebalancing the entire portfolio less frequently
- Buying/Selling Large Volumes can affect prices
- Overhead of additional calculations & trading

# Issues with the Dataset
- The model doesn't account for transaction costs
- Lack of individual stock weight caps can lead to excessive concentration in a few very large cap stocks.
- There's no buffer around the threshold to prevent excessive turnover when hovering around a threshold

# Issues with the Code
- I don't handle all edge cases when parsing csv files - e.g. empty files, files with correct headers but no rows.
- Calculations with float64 can lead to small rounding errors over time
- I don't take into account companies with a market cap of 0
- my date filtering allows for potentially invalid dates - e.g. "99/99/9999"
- I perform frequent lookups by company name without using indexes which will be inefficient for large datasets
- 