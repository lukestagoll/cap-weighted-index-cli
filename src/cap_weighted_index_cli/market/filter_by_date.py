import re
from pandas import DataFrame, Timestamp

def filter_by_date(market_data: DataFrame, date: Timestamp | str) -> DataFrame:
    """Filters the DataFrame to rows where the date field matches the specified date.

    Args:
        market_data (DataFrame): The input DataFrame containing a date field.
        date (str): The date value to match (e.g., '01/01/2025').

    Returns:
        DataFrame: A filtered DataFrame containing only rows where the date field equals `date`.

    Raises:
        KeyError: If the `date` column does not exist in the DataFrame.
    """
    
    if not isinstance(market_data, DataFrame):
        raise TypeError("`market_data` must be a DataFrame")

    if (not isinstance(date, Timestamp) and not isinstance(date, str)) or (isinstance(date, str) and not re.fullmatch(r"\d{2}/\d{2}/\d{4}", date)):
        raise TypeError("`date` must be a Timestamp or a date string in the format \"DD/MM/YYYY\"")
    
    if "date" not in market_data.columns:
        raise KeyError("`date` column not found in `market_data`")
    
    return market_data[market_data["date"] == date]