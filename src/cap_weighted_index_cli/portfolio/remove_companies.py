from typing import Set
from pandas import DataFrame
from numpy import float64, floor

def remove_companies(portfolio: DataFrame, companies: Set[str]) -> DataFrame:
    """Removes companies from the portfolio and returns the updated portfolio

    Args:
        portfolio (DataFrame): The DataFrame to update.
        companies (Set[str]): A set of company names to remove from the portfolio

    Returns:
        DataFrame: The updated DataFrame.

    Raises:
        KeyError: If the `company` column does not exist in the DataFrame.
        TypeError: If `portfolio` is not a DataFrame or `companies` is not a set of strings.
    """

    if not isinstance(portfolio, DataFrame):
        raise TypeError("`portfolio` must be a DataFrame")

    if not isinstance(companies, Set) or not all(isinstance(item, str) for item in companies):
        raise TypeError("`companies` must be a set of strings")

    if "company" not in portfolio.columns:
        raise KeyError("`company` column not found in `portfolio`")
    
    portfolio = portfolio[~portfolio["company"].isin(companies)]
    return portfolio