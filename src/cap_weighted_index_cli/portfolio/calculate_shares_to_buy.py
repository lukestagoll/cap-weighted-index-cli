from pandas import DataFrame
from numpy import float64, floor

def calculate_shares_to_buy(portfolio: DataFrame, available_funds: float64) -> DataFrame:
    """Calculates the number of shares to buy for each company in the DataFrame by multiplying the available_funds
    by the weight of the company and multiplying by the price of the company's shares

    Args:
        portfolio (DataFrame): The DataFrame to perform the calculation on.

    Returns:
        DataFrame: The updated DataFrame with a new `shares` column, or updated `shares` values.

    Raises:
        KeyError: If the `weight` and `price` column does not exist in the DataFrame.
    """

    if not isinstance(portfolio, DataFrame):
        raise TypeError("`portfolio` must be a DataFrame")

    if not isinstance(available_funds, float64) or available_funds <= float64(0.0):
        raise TypeError("`available_funds` must be a float64 greater than 0")

    if "weight" not in portfolio.columns:
        raise KeyError("`weight` column not found in `portfolio`")
    
    if "price" not in portfolio.columns:
        raise KeyError("`price` column not found in `portfolio`")
    
    portfolio["shares"] = floor(available_funds * portfolio["weight"] / portfolio["price"]).astype("int")
    return portfolio