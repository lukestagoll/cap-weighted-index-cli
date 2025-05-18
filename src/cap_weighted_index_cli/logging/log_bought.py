from numpy import float64
from pandas import DataFrame, Timestamp
from rich.table import Table

from cap_weighted_index_cli.logging.logger import get_console

def log_bought(shares_to_buy: DataFrame, available_funds: float64):
    console = get_console()
    
    console.print("\nBought:")
    for index, row in shares_to_buy.iterrows():
        console.print(f"\t-> '{row["shares"]:,}' units of '{row["company"]}' at '${row["price"]:.2f}' for a total of '${row["value"]:,.2f}'")
    
    console.print(f"\t-> Funds Available After Buying: '${available_funds:,.2f}'")
        