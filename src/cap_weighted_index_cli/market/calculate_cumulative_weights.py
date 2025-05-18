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
    
    if not isinstance(market_data, DataFrame):
        raise TypeError("`market_data` must be a DataFrame")

    if "weight" not in market_data.columns:
        raise KeyError("`weight` column not found in `market_data`")
    
    market_data["cumulative_weight"] = market_data["weight"].cumsum()
    return market_data