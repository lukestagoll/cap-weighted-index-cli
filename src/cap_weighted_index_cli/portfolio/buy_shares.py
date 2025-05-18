from typing import Tuple
from pandas import DataFrame
from numpy import float64

def buy_shares(portfolio: DataFrame, available_funds: float64) -> Tuple[DataFrame, float64]:
    """if portfolio["value"] is empty, set portfolio["value"] and subtract from available_funds 

    Args:
        portfolio (DataFrame): The DataFrame to perform the calculation on, where the `value` column has not been defined.
        available_funds (float64): Number of funds available to spend

    Returns:
        Tuple[DataFrame, float64]: A tuple where the first value is the updated DataFrame with a new `value` column,
        and the second value is number of funds remaining after purchase

    Raises:
        KeyError: If the `shares` and `price` column do not exist in the DataFrame, or if the `value column has already been defined.
        TypeError: If `portfolio` is not a DataFrame or `available_funds` is not a float64 greater than 0
    """

    if not isinstance(portfolio, DataFrame):
        raise TypeError("`portfolio` must be a DataFrame")

    if not isinstance(available_funds, float64) or available_funds <= float64(0.0):
        raise TypeError("`available_funds` must be a float64 greater than 0")

    if "value" in portfolio.columns:
        raise KeyError("`value` column has already been defined in `portfolio`")

    if "shares" not in portfolio.columns:
        raise KeyError("`shares` column not found in `portfolio`")
    
    if "price" not in portfolio.columns:
        raise KeyError("`price` column not found in `portfolio`")
    
    portfolio["value"] = (portfolio["shares"] * portfolio["price"]).astype("float64")
    funds_remaining = available_funds - portfolio["value"].sum()
    return portfolio, funds_remaining