from pandas import DataFrame

def calculate_weights(market_data: DataFrame, total_market_cap: int) -> DataFrame:
    """Calculates the weight of each company in the DataFrame by dividing `market_cap_m` by `total_market_cap`

    Args:
        market_data (DataFrame): The DataFrame to perform the calculation on.

    Returns:
        DataFrame: The updated DataFrame with a new `weight` column, or updated `weight` values.

    Raises:
        KeyError: If the `market_cap_m` column does not exist in the DataFrame.
        TypeError: If `market_data` is not a DataFrame or `total_market_cap` is not an int.
    """

    if not isinstance(market_data, DataFrame):
        raise TypeError("`market_data` must be a DataFrame")

    if not isinstance(total_market_cap, int):
        raise TypeError("`total_market_cap` must be an int")

    if "market_cap_m" not in market_data.columns:
        raise KeyError("`market_cap_m` column not found in `market_data`")
    
    market_data["weight"] = (market_data["market_cap_m"] / total_market_cap).astype("float64")
    return market_data