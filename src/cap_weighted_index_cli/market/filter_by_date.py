from pandas import DataFrame

def filter_by_date(market_data: DataFrame, date: str) -> DataFrame:
    """Filters the DataFrame to rows where the date field matches the specified date.

    Args:
        market_data (DataFrame): The input DataFrame containing a date field.
        date (str): The date value to match (e.g., '01/01/2025').

    Returns:
        DataFrame: A filtered DataFrame containing only rows where the date field equals `date`.

    Raises:
        KeyError: If the `date` column does not exist in the DataFrame.
    """
    return market_data[market_data["date"] == date]