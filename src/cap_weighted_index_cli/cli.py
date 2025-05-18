#!/usr/bin/env python

import sys
import click
from numpy import float64
from cap_weighted_index_cli.data.parse_csv import parse_csv
from cap_weighted_index_cli.execution.trade import trade
from cap_weighted_index_cli.logging.logger import get_console, log_error

@click.command(context_settings={ "ignore_unknown_options": True })
@click.option(
    "--input", "-i",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    default="data/input/market_capitalisation.csv",
    show_default=True,
    help="Input file path (CSV)"
)
@click.option(
    "--available-funds",
    type=float,
    default=100000000.00,
    show_default=True,
    help="The amount of funds available to invest."
)
@click.option(
    "--max-cumulative-weight",
    type=click.FloatRange(0.00, 0.85),
    default=0.85,
    show_default=True,
    help="Only invest in companies within this threshold (0.00 - 1.00)"
)
def main(input: str, available_funds: float, max_cumulative_weight: float):
    """Market Cap Index - A tool for calculating market cap weighted indices."""
    try:
        console = get_console()
        console.print(f"Reading Market Data From: {input!r}")

        market_data = parse_csv(input)
        if market_data is None:
            sys.exit(1)
            
        console.print("Processing...")
        
        trade(market_data, float64(available_funds), float64(max_cumulative_weight))

    except ValueError as e:
        log_error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
