from numpy import float64
from pandas import DataFrame

def filter_by_cumulative_weight(market_data: DataFrame, max_cumulative_weight: float64) -> DataFrame:
    """Filters the DataFrame to contain rows where the `cumulative_weight` is less than or equal to `max_cumulative_weight

    Args:
        market_data (DataFrame): The DataFrame to perform the calculation on.
        max_cumulative_weight (float64): The maximum allowed value of `cumulative_weight`

    Returns:
        DataFrame: A new DataFrame where each rows `cumulative_weight` is less than or equal to `max_cumulative_weight`

    Raises:
        KeyError: If the `cumulative_weight` column does not exist in the DataFrame.
    """
    return market_data[market_data["cumulative_weight"] <= max_cumulative_weight]