from pandas import DataFrame

def calculate_total_market_cap(market_data: DataFrame) -> int:
    """Sums the values of `market_cap_m` and returns the result

    Args:
        market_data (DataFrame): The DataFrame to perform the calculation on.

    Returns:
        int: the total market cap

    Raises:
        KeyError: If the market_cap_m column does not exist in the DataFrame.
    """

    if not isinstance(market_data, DataFrame):
        raise TypeError("`market_data` must be a DataFrame")

    if "market_cap_m" not in market_data.columns:
        raise KeyError("`market_cap_m` column not found in `market_data`")

    return market_data["market_cap_m"].sum()