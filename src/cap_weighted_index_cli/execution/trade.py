from typing import List, Set, Tuple
from numpy import float64
from pandas import DataFrame, Timestamp

from cap_weighted_index_cli.market.get_dates import get_dates
from cap_weighted_index_cli.market.prepare_market_snapshot import prepare_market_snapshot
from cap_weighted_index_cli.portfolio.calculate_value import calculate_value
from cap_weighted_index_cli.portfolio.identify_portfolio_changes import identify_portfolio_changes
from cap_weighted_index_cli.execution.buy import buy
from cap_weighted_index_cli.execution.sell import sell
from cap_weighted_index_cli.logging.log_profit import log_profit
from cap_weighted_index_cli.logging.log_portfolio import log_portfolio
from cap_weighted_index_cli.logging.logger import get_console

def trade(market_data: DataFrame, available_funds: float64, max_cumulative_weight: float64):
    """
    Execute trades to maintain a cap-weighted index portfolio over time.
    
    This function processes market data sequentially by date, making buy and sell decisions
    to maintain a portfolio that tracks a capitalization-weighted index. For each trading date,
    it prepares market snapshots, identifies necessary portfolio changes, executes sales and 
    purchases, and logs the updated portfolio state.
    
    Args:
        market_data: DataFrame containing market data with dates, securities, and market caps
        available_funds: Initial cash available for investment
        max_cumulative_weight: Maximum cumulative market cap weight threshold for index inclusion
        
    Returns:
        None. Results are logged to the configured logger.
        
    Flow:
        1. Extract trading dates from market data
        2. For each date:
           a. Prepare market snapshots (full and filtered by weight threshold)
           b. Identify securities to buy and sell based on portfolio changes
           c. Execute sell orders first, then buy orders
           d. Calculate updated portfolio value
           e. Log portfolio status
    """
    dates: List[Timestamp] = get_dates(market_data)
    
    portfolio = DataFrame()
    console = get_console()
    
    funds_start = available_funds
    portfolio_value = available_funds
    
    for date in dates:
        console.rule()
        console.print(f"Date: {date}")
        market_snapshot, filtered_market_data = prepare_market_snapshot(market_data, date, max_cumulative_weight)
        
        to_sell, to_buy = identify_portfolio_changes(portfolio, filtered_market_data)
        
        portfolio, available_funds = sell(portfolio, market_snapshot, to_sell, available_funds)
        portfolio, available_funds = buy(portfolio, filtered_market_data, to_buy, available_funds)
        
        portfolio_value = calculate_value(portfolio, available_funds)

        log_portfolio(portfolio, date)
        
    log_profit(funds_start, portfolio_value)