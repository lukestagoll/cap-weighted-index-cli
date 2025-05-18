from pandas import DataFrame

def calculate_cumulative_weights(market_data: DataFrame) -> DataFrame:
    """Calculates the cumulative weight of each company in the DataFrame

    Args:
        market_data (DataFrame): The DataFrame to perform the calculation on.

    Returns:
        DataFrame: The updated DataFrame with a new `cumulative_weight` column, or updated `cumulative_weight` values.

    Raises:
        KeyError: If the `weight` column does not exist in the DataFrame.
    """
    market_data["cumulative_weight"] = market_data["weight"].cumsum()
    return market_data