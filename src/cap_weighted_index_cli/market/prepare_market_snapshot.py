from typing import Tuple
from numpy import float64
from pandas import DataFrame, Timestamp

from cap_weighted_index_cli.market.filter_by_date import filter_by_date
from cap_weighted_index_cli.market.sort_by_market_cap import sort_by_market_cap
from cap_weighted_index_cli.market.calculate_total_market_cap import calculate_total_market_cap
from cap_weighted_index_cli.analysis.calculate_weights import calculate_weights
from cap_weighted_index_cli.analysis.calculate_cumulative_weights import calculate_cumulative_weights
from cap_weighted_index_cli.analysis.filter_by_cumulative_weight import filter_by_cumulative_weight

def prepare_market_snapshot(market_data: DataFrame, date: Timestamp, max_cumulative_weight: float64) -> Tuple[DataFrame, DataFrame]:
    """
    Process market data for a specific date to prepare it for trading decisions.
    
    Args:
        market_data: The full market dataset
        date: The specific date to process
        max_cumulative_weight: Maximum cumulative weight threshold
        
    Returns:
        Tuple containing:
            - The complete market snapshot with calculated weights
            - The filtered market snapshot containing only securities within the cumulative weight threshold
    """
    market_snapshot = filter_by_date(market_data, date)
    market_snapshot = sort_by_market_cap(market_snapshot)
    total_market_cap = calculate_total_market_cap(market_snapshot)
    market_snapshot = calculate_weights(market_snapshot, total_market_cap)
    market_snapshot = calculate_cumulative_weights(market_snapshot)
    return market_snapshot, filter_by_cumulative_weight(market_snapshot, max_cumulative_weight)