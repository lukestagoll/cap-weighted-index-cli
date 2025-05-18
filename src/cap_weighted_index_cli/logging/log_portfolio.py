from pandas import DataFrame, Timestamp
from rich.table import Table

from cap_weighted_index_cli.logging.logger import get_console, log_info

def log_portfolio(portfolio: DataFrame, date: Timestamp) -> None:
    console = get_console()

    table = Table(title=f"\nPortfolio on {date}", style="white")
    table.add_column("Company", style="blue")
    table.add_column("Price", style="magenta")
    table.add_column("Shares Owned", style="green")
    table.add_column("Value", style="cyan")

    for index, row in portfolio.iterrows():
        table.add_row(row["company"], f"${row["price"]:,.2f}", f"{row["shares"]:,}", f"${row["value"]:,.2f}")
        
    console.print(table)