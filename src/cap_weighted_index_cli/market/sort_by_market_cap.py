from pandas import DataFrame

def sort_by_market_cap(market_data: DataFrame) -> DataFrame:
    """Sorts the DataFrame by `market_cap_m` in descending order

    Args:
        market_data (DataFrame): The DataFrame to sort.

    Returns:
        DataFrame: A DataFrame sorted by `market_cap_m` in descending order

    Raises:
        KeyError: If the `market_cap_m` column does not exist in the DataFrame.
    """
    return market_data.sort_values(by="market_cap_m", ascending=False)