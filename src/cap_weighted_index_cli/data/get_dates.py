from typing import List
from pandas import DataFrame
from pandera import Timestamp

def get_dates(market_data: DataFrame) -> List[Timestamp]:
    """Extracts a sorted list of unique dates from the 'date' column of a DataFrame.

    Args:
        market_data (DataFrame): A DataFrame containing a 'date' column 
            with datetime-like values (e.g. pd.Timestamp).

    Returns:
        List[Timestamp]: A list of unique dates in ascending order.
    """
    dates = market_data["date"].drop_duplicates().sort_values()
    return dates.tolist()