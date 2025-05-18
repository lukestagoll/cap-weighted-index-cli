from pandas import DataFrame
from numpy import float64, floor

def calculate_value(portfolio: DataFrame, available_funds: float64) -> float64:
    """Calculates the total value of the portfolio & available_funds

    Args:
        portfolio (DataFrame): The DataFrame to perform the calculation on.
        available_funds (float64): The amount of funds available to invest

    Returns:
        float64: the total value of the portfolio & available_funds

    Raises:
        KeyError: If the `value` column does not exist in the DataFrame.
        TypeError: If `portfolio` is not a DataFrame.
    """

    if not isinstance(portfolio, DataFrame):
        raise TypeError("`portfolio` must be a DataFrame")

    if not isinstance(available_funds, float64) or available_funds < float64(0.0):
        raise TypeError("`available_funds` must be a float64 greater than or equal to 0")

    if "value" not in portfolio.columns:
        raise KeyError("`value` column not found in `portfolio`")
    
    return available_funds + portfolio["value"].sum()