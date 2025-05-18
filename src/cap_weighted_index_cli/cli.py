#!/usr/bin/env python

import click

@click.command(context_settings={ "ignore_unknown_options": True })
@click.option(
    "--input", "-i",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    default="data/input/market_capitalisation.csv",
    show_default=True,
    help="Input file path (CSV)"
)
@click.option(
    "--output", "-o",
    type=click.Path(exists=False, file_okay=True, dir_okay=False, writable=True, resolve_path=True),
    default="data/output/results.csv",
    show_default=True,
    help="File where results will be written (CSV)"
)
@click.option(
    "--no-output",
    is_flag=True,
    default=False,
    help="Skip writing CSV; Only print results to stdout."
)
def main(input: str, output: str, no_output: bool):
    """Market Cap Index - A tool for calculating market cap weighted indices."""

    click.echo(f"Reading from {input!r}")

if __name__ == "__main__":
    main()
