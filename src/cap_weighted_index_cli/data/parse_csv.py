from typing import Optional
import pandas as pd
import warnings
import logging
from pandera.errors import SchemaError
from cap_weighted_index_cli.models.market_model import MarketModel

logger = logging.getLogger(__name__)

def parse_csv(file_path: str) -> Optional[pd.DataFrame]:
    """Parse a CSV file into a pandas DataFrame and validates it against MarketModel
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        Optional[DataFrame]: Pandas DataFrame containing the CSV data, or None if an error occurs
    """
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            df: pd.DataFrame = pd.read_csv(file_path)
            validated_df = MarketModel.validate(df)
        return validated_df
    except SchemaError as e:
        logging.error(
            "CSV format is invalid.\nExpected format:\n"
            "\t- 'date': valid date in the format DD/MM/YYYY\n"
            "\t- 'company': non-empty string\n"
            "\t- 'market_cap_m': non-negative number\n"
            "\t- 'price': non-negative number\n"
        )
        return None
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None