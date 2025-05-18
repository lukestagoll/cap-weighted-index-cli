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
    return market_data["market_cap_m"].sum()