from typing import Tuple
from pandas import DataFrame
from numpy import float64

def sell_shares(shares_to_sell: DataFrame, available_funds: float64) -> Tuple[DataFrame, float64]:
    """if shares_to_sell["value"] is empty, set shares_to_sell["value"] and subtract from available_funds 

    Args:
        shares_to_sell (DataFrame): The DataFrame to perform the calculation on.
        available_funds (float64): Number of funds available to spend

    Returns:
        Tuple[DataFrame, float64]: A tuple where the first value is the updated DataFrame with a new `value` column,
        and the second value is number of funds remaining after purchase

    Raises:
        KeyError: If the `shares` and `price` column do not exist in the DataFrame.
        TypeError: If `shares_to_sell` is not a DataFrame or `available_funds` is not a float64 greater than or equal to 0
    """

    if not isinstance(shares_to_sell, DataFrame):
        raise TypeError("`shares_to_sell` must be a DataFrame")

    if not isinstance(available_funds, float64) or available_funds < float64(0.0):
        raise TypeError("`available_funds` must be a float64 greater than or equal to 0")

    if "shares" not in shares_to_sell.columns:
        raise KeyError("`shares` column not found in `shares_to_sell`")
    
    if "price" not in shares_to_sell.columns:
        raise KeyError("`price` column not found in `shares_to_sell`")

    result = shares_to_sell.copy()
    result.loc[:, "value"] = (shares_to_sell["shares"] * shares_to_sell["price"]).astype("float64")
    funds_remaining = available_funds + result["value"].sum()
    return result, funds_remaining