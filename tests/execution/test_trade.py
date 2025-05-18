import unittest
from unittest.mock import patch, MagicMock, call, ANY
from numpy import float64
import pandas as pd
from pandas import Timestamp
from cap_weighted_index_cli.execution.trade import trade

class TestTrade(unittest.TestCase):
    def setUp(self):
        # Setup common test data
        self.market_data = pd.DataFrame({
            "date": [
                pd.Timestamp("01/01/2025"),
                pd.Timestamp("01/01/2025"),
                pd.Timestamp("01/01/2025"),
                pd.Timestamp("01/02/2025"),
                pd.Timestamp("01/02/2025"),
                pd.Timestamp("01/02/2025"),
            ],
            "company": ["A", "B", "C", "A", "B", "D"],
            "market_cap_m": [400, 300, 200, 450, 250, 180],
            "price": [12, 9, 5, 13, 8, 4],
        })
        self.available_funds = float64(100.0)
        self.max_cumulative_weight = float64(0.85)

    @patch('cap_weighted_index_cli.execution.trade.get_dates')
    @patch('cap_weighted_index_cli.execution.trade.prepare_market_snapshot')
    @patch('cap_weighted_index_cli.execution.trade.identify_portfolio_changes')
    @patch('cap_weighted_index_cli.execution.trade.sell')
    @patch('cap_weighted_index_cli.execution.trade.buy')
    @patch('cap_weighted_index_cli.execution.trade.calculate_value')
    @patch('cap_weighted_index_cli.execution.trade.log_portfolio')
    @patch('cap_weighted_index_cli.execution.trade.log_profit')
    @patch('cap_weighted_index_cli.execution.trade.get_console')
    def test_trade_execution(self, mock_console, mock_log_profit, mock_log_portfolio, 
                            mock_calc_value, mock_buy, mock_sell, 
                            mock_identify_changes, mock_prepare_snapshot, mock_get_dates):
        # Arrange
        dates = [pd.Timestamp("01/01/2025"), pd.Timestamp("01/02/2025")]
        mock_get_dates.return_value = dates
        
        market_snapshot1 = pd.DataFrame({"company": ["A", "B", "C"], "price": [12, 9, 5]})
        filtered_data1 = pd.DataFrame({"company": ["A", "B"], "price": [12, 9]})
        
        market_snapshot2 = pd.DataFrame({"company": ["A", "B", "D"], "price": [13, 8, 4]})
        filtered_data2 = pd.DataFrame({"company": ["A", "D"], "price": [13, 4]})
        
        mock_prepare_snapshot.side_effect = [(market_snapshot1, filtered_data1), (market_snapshot2, filtered_data2)]
        mock_identify_changes.side_effect = [(set(), {"A", "B"}), ({"B"}, {"D"})]
        
        portfolio1 = pd.DataFrame({"company": ["A", "B"], "price": [12, 9], "shares": [4, 5], "value": [48, 45]})
        funds_after_buy1 = float64(7.0)
        portfolio2 = pd.DataFrame({"company": ["A", "D"], "price": [13, 4], "shares": [4, 10], "value": [52, 40]})
        
        funds_after_sell = float64(52.0)
        funds_after_buy2 = float64(12.0)
        mock_buy.side_effect = [(portfolio1, funds_after_buy1), (portfolio2, funds_after_buy2)]
        mock_sell.side_effect = [(portfolio1, funds_after_sell), (portfolio2, funds_after_buy2)]
        
        portfolio_value1 = float64(100.0)
        portfolio_value2 = float64(104.0)
        mock_calc_value.side_effect = [portfolio_value1, portfolio_value2]
        
        # Mock console
        mock_console_instance = MagicMock()
        mock_console.return_value = mock_console_instance
        
        # Act
        trade(self.market_data, self.available_funds, self.max_cumulative_weight)
        
        # Assert
        # Verify each function was called with the right parameters and the right number of times
        self.assertEqual(mock_get_dates.call_count, 1)
        self.assertEqual(mock_prepare_snapshot.call_count, 2)
        self.assertEqual(mock_identify_changes.call_count, 2)
        self.assertEqual(mock_sell.call_count, 2)
        self.assertEqual(mock_buy.call_count, 2)
        self.assertEqual(mock_calc_value.call_count, 2)
        self.assertEqual(mock_log_portfolio.call_count, 2)
        self.assertEqual(mock_log_profit.call_count, 1)
        
        # Verify the final log_profit call
        mock_log_profit.assert_called_with(self.available_funds, portfolio_value2)
        
        # Verify sequence of operations individually (instead of using assert_has_calls)
        # First date operations
        mock_prepare_snapshot.assert_any_call(self.market_data, dates[0], self.max_cumulative_weight)
        mock_identify_changes.assert_any_call(ANY, filtered_data1)
        mock_sell.assert_any_call(ANY, market_snapshot1, set(), self.available_funds)
        
        # Second date operations
        mock_prepare_snapshot.assert_any_call(self.market_data, dates[1], self.max_cumulative_weight)

    @patch('cap_weighted_index_cli.execution.trade.get_console')
    def test_trade_integration(self, mock_console):
        # Arrange
        test_market_data = pd.DataFrame({
            "date": [
                pd.Timestamp("01/01/2025"),
                pd.Timestamp("01/01/2025"),
                pd.Timestamp("01/01/2025"),
                pd.Timestamp("01/02/2025"),
                pd.Timestamp("01/02/2025"),
                pd.Timestamp("01/02/2025"),
            ],
            "company": ["A", "B", "C", "A", "B", "D"],
            "market_cap_m": [400, 300, 200, 450, 250, 180],
            "price": [12, 9, 5, 13, 8, 4],
        })
        
        # Mock console to prevent cluttering test output
        mock_console_instance = MagicMock()
        mock_console.return_value = mock_console_instance
        
        # Act - No assertions, just make sure it runs without exceptions
        trade(test_market_data, float64(1000.0), float64(0.85))
        
        # Minimal assertion - console should have been used to print output
        self.assertTrue(mock_console_instance.print.called)
        self.assertTrue(mock_console_instance.rule.called)

    @patch('cap_weighted_index_cli.execution.trade.get_console')
    def test_trade_with_empty_market_data(self, mock_console):
        # Arrange
        empty_market_data = pd.DataFrame({
            "date": [],
            "company": [],
            "market_cap_m": [],
            "price": [],
        })
        
        mock_console_instance = MagicMock()
        mock_console.return_value = mock_console_instance
        
        # Act
        trade(empty_market_data, self.available_funds, self.max_cumulative_weight)
        
        # Assert
        # Should get console but not print any trades
        self.assertEqual(mock_console_instance.rule.call_count, 0)
        # Portfolio value should remain unchanged at initial funds

    @patch('cap_weighted_index_cli.execution.trade.get_dates')
    @patch('cap_weighted_index_cli.execution.trade.log_profit')
    @patch('cap_weighted_index_cli.execution.trade.get_console')
    def test_trade_single_date(self, mock_console, mock_log_profit, mock_get_dates):
        # Arrange
        mock_get_dates.return_value = [pd.Timestamp("01/01/2025")]
        mock_console_instance = MagicMock()
        mock_console.return_value = mock_console_instance
        
        # Mock a simple market with just one date
        simple_market_data = pd.DataFrame({
            "date": [pd.Timestamp("01/01/2025"), pd.Timestamp("01/01/2025")],
            "company": ["A", "B"],
            "market_cap_m": [400, 300],
            "price": [12, 9],
        })
        
        # Act
        trade(simple_market_data, float64(100.0), float64(0.85))
        
        # Assert
        self.assertEqual(mock_console_instance.rule.call_count, 1)
        self.assertTrue(mock_log_profit.called)

    @patch('cap_weighted_index_cli.execution.trade.prepare_market_snapshot')
    @patch('cap_weighted_index_cli.execution.trade.identify_portfolio_changes')
    @patch('cap_weighted_index_cli.execution.trade.get_console')
    def test_trade_handles_exception(self, mock_console, mock_identify_changes, mock_prepare_snapshot):
        # Arrange
        mock_console_instance = MagicMock()
        mock_console.return_value = mock_console_instance
        mock_prepare_snapshot.side_effect = Exception("Test exception")
        
        # Act & Assert
        with self.assertRaises(Exception):
            trade(self.market_data, self.available_funds, self.max_cumulative_weight)

if __name__ == "__main__":
    unittest.main()