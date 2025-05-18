from typing import Set, Tuple
from pandas import DataFrame
from numpy import float64, floor

def identify_portfolio_changes(portfolio: DataFrame, filtered_market_data: DataFrame) -> Tuple[Set[str], Set[str]]:
    """Removes companies from the portfolio and returns the updated portfolio

    Args:
        portfolio (DataFrame): The existing DataFrame portfolio.
        filtered_market_data (DataFrame): The current market data

    Returns:
        Tuple[Set[str], Set[str]]: A tuple where the first value is a set of companies in the portfolio to sell,
        the second value is a set of companies in the filtered_market_data to invest in.

    Raises:
        KeyError: If the `company` column does not exist in filtered_market_data.
        TypeError: If `portfolio` is not a DataFrame or `filtered_market_data` is not a DataFrame
    """

    if not isinstance(portfolio, DataFrame):
        raise TypeError("`portfolio` must be a DataFrame")

    if not isinstance(filtered_market_data, DataFrame):
        raise TypeError("`filtered_market_data` must be a DataFrame")
    
    if "company" not in filtered_market_data.columns:
        raise KeyError("`company` column not found in `filtered_market_data`")
    
    companies_invested_in = set()
    if "company" in portfolio:
        companies_invested_in = set(portfolio["company"])

    companies_to_invest = set(filtered_market_data["company"])
    
    to_sell = companies_invested_in - companies_to_invest
    to_buy = companies_to_invest - companies_invested_in
    return to_sell, to_buy