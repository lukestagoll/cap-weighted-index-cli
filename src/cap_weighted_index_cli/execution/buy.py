import logging
from typing import Set, Tuple
from numpy import float64
from pandas import DataFrame

from cap_weighted_index_cli.portfolio.calculate_shares_to_buy import calculate_shares_to_buy
from cap_weighted_index_cli.portfolio.buy_shares import buy_shares

def buy(portfolio: DataFrame, market_snapshot: DataFrame, to_buy: Set[str], available_funds: float64) -> Tuple[DataFrame, float64]:
    companies_to_invest_in = market_snapshot[market_snapshot["company"].isin(to_buy)]
    shares_to_buy = calculate_shares_to_buy(companies_to_invest_in, available_funds)

    portfolio, available_funds = buy_shares(portfolio, shares_to_buy, available_funds)

    return portfolio, available_funds