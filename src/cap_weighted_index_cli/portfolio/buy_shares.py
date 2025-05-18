from typing import Tuple
from pandas import DataFrame, concat
from numpy import float64

def buy_shares(portfolio: DataFrame, shares_to_buy: DataFrame, available_funds: float64) -> Tuple[DataFrame, float64]:
    """Buys shares specified in shares_to_buy DataFrame and adds them to the portfolio.

    Args:
        portfolio (DataFrame): The current portfolio DataFrame that must contain a 'company' column.
        shares_to_buy (DataFrame): DataFrame with companies to purchase, must contain 'company', 'shares', and 'price' columns.
        available_funds (float64): Amount of funds available to spend on the purchases.

    Returns:
        Tuple[DataFrame, float64]: A tuple where the first value is the updated portfolio with the new shares added,
        and the second value is the amount of funds remaining after purchase.

    Raises:
        KeyError: If required columns don't exist in the DataFrames.
        TypeError: If portfolio or shares_to_buy are not DataFrames, or if available_funds is not a positive float64.
        ValueError: If shares_to_buy contains companies that already exist in the portfolio.
    """

    if not isinstance(portfolio, DataFrame):
        raise TypeError("`portfolio` must be a DataFrame")

    if not isinstance(shares_to_buy, DataFrame):
        raise TypeError("`shares_to_buy` must be a DataFrame")

    if not isinstance(available_funds, float64) or available_funds <= float64(0.0):
        raise TypeError("`available_funds` must be a float64 greater than 0")
    
    if "company" not in portfolio.columns:
        raise KeyError("`company` column not found in `portfolio`")

    if "company" not in shares_to_buy.columns:
        raise KeyError("`company` column not found in `shares_to_buy`")

    if "shares" not in shares_to_buy.columns:
        raise KeyError("`shares` column not found in `shares_to_buy`")
    
    if "price" not in shares_to_buy.columns:
        raise KeyError("`price` column not found in `shares_to_buy`")
    
    if not set(portfolio["company"]).isdisjoint(set(shares_to_buy["company"])):
        raise ValueError("`shares_to_buy` cannot contain companies that exist in `portfolio`")
    
    shares_to_buy["value"] = (shares_to_buy["shares"] * shares_to_buy["price"]).astype("float64")
    funds_remaining = available_funds - shares_to_buy["value"].sum()
    
    portfolio = concat([portfolio, shares_to_buy], ignore_index=True)
    return portfolio, funds_remaining