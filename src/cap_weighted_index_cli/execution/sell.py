import logging
from typing import Set, Tuple
from numpy import float64
from pandas import DataFrame

from cap_weighted_index_cli.portfolio.sell_shares import sell_shares
from cap_weighted_index_cli.portfolio.remove_companies import remove_companies
from cap_weighted_index_cli.logging.log_sold import log_sold

def sell(portfolio: DataFrame, market_snapshot: DataFrame, to_sell: Set[str], available_funds: float64) -> Tuple[DataFrame, float64]:
    if not portfolio.empty:
        columns_to_update = ["date", "market_cap_m", "price", "weight", "cumulative_weight"]
        
        # Create a mapping of company to row index for efficient lookup
        company_to_idx = {company: idx for idx, company in enumerate(portfolio["company"])}

        # Get companies that exist in both portfolio and market_snapshot
        common_companies = set(portfolio["company"]) & set(market_snapshot["company"])

        # Update each column for each common company
        for company in common_companies:
            portfolio_idx = company_to_idx[company]
            market_idx = market_snapshot.loc[market_snapshot["company"] == company].index[0]
            
            for column in columns_to_update:
                portfolio.loc[portfolio_idx, column] = market_snapshot.loc[market_idx, column]

        shares_to_sell = portfolio[portfolio["company"].isin(to_sell)]
        sold, available_funds = sell_shares(shares_to_sell, available_funds)
        log_sold(sold, available_funds)
        portfolio = remove_companies(portfolio, to_sell)
    
    return portfolio, available_funds