from pandas import DataFrame

def sort_by_market_cap(market_data: DataFrame) -> DataFrame:
    """Sorts the DataFrame by `market_cap_m` in descending order

    Args:
        market_data (DataFrame): The DataFrame to sort.

    Returns:
        DataFrame: A DataFrame sorted by `market_cap_m` in descending order

    Raises:
        KeyError: If the `market_cap_m` column does not exist in the DataFrame.
        TypeError: If `market_data` is not a DataFrame.
    """
    
    if not isinstance(market_data, DataFrame):
        raise TypeError("`market_data` must be a DataFrame")

    if "market_cap_m" not in market_data.columns:
        raise KeyError("`market_cap_m` column not found in `market_data`")
    
    return market_data.sort_values(by="market_cap_m", ascending=False)