import unittest
from unittest.mock import patch, MagicMock
from numpy import float64
import pandas as pd
import pandas.testing as pdt
from cap_weighted_index_cli.execution.sell import sell

class TestSell(unittest.TestCase):
    def setUp(self):
        # Setup initial test data
        self.portfolio = pd.DataFrame({
            "company": ["A", "B", "C"],
            "price": [10, 8, 5],
            "shares": [4, 3, 2],
            "value": [float64(40), float64(24), float64(10)],
        })
        
        self.market_snapshot = pd.DataFrame({
            "company": ["A", "B", "C", "D"],
            "date": ["01/01/2025", "01/01/2025", "01/01/2025", "01/01/2025"],
            "price": [12, 9, 6, 3],
            "market_cap_m": [400, 300, 200, 100],
            "weight": [0.4, 0.3, 0.2, 0.1],
            "cumulative_weight": [0.4, 0.7, 0.9, 1.0],
        })

    @patch('cap_weighted_index_cli.execution.sell.sell_shares')
    @patch('cap_weighted_index_cli.execution.sell.remove_companies')
    @patch('cap_weighted_index_cli.execution.sell.log_sold')
    def test_sell_normal_execution(self, mock_log_sold, mock_remove_companies, mock_sell_shares):
        # Arrange
        to_sell = {"B", "C"}
        available_funds = float64(100.0)
        
        mock_sold = pd.DataFrame({
            "company": ["B", "C"],
            "price": [9, 6],
            "shares": [3, 2],
            "value": [float64(27), float64(12)]
        })
        
        expected_funds = float64(139.0)
        expected_portfolio = pd.DataFrame({
            "company": ["A"],
            "price": [12],
            "shares": [4],
            "value": [float64(48)],
        })
        
        mock_sell_shares.return_value = (mock_sold, expected_funds)
        mock_remove_companies.return_value = expected_portfolio
        
        # Act
        result_portfolio, result_funds = sell(self.portfolio, self.market_snapshot, to_sell, available_funds)
        
        # Assert
        self.assertEqual(mock_sell_shares.call_count, 1)
        self.assertEqual(mock_remove_companies.call_count, 1)
        self.assertEqual(mock_log_sold.call_count, 1)
        pdt.assert_frame_equal(result_portfolio, expected_portfolio)
        self.assertEqual(result_funds, expected_funds)
        
        # Verify the portfolio prices were updated before selling
        sell_shares_args = mock_sell_shares.call_args[0]
        shares_to_sell = sell_shares_args[0]
        # Price should be updated from market_snapshot
        self.assertEqual(shares_to_sell.loc[shares_to_sell["company"] == "B", "price"].iloc[0], 9)
        self.assertEqual(shares_to_sell.loc[shares_to_sell["company"] == "C", "price"].iloc[0], 6)

    def test_sell_integration(self):
        # Arrange
        to_sell = {"B", "C"}
        available_funds = float64(100.0)
        
        # Act
        result_portfolio, result_funds = sell(self.portfolio, self.market_snapshot, to_sell, available_funds)
        
        # Assert
        # Check companies B and C were removed
        self.assertFalse("B" in result_portfolio["company"].values)
        self.assertFalse("C" in result_portfolio["company"].values)
        self.assertTrue("A" in result_portfolio["company"].values)
        self.assertEqual(len(result_portfolio), 1)
        self.assertGreater(float(result_funds), float(available_funds))
        # Price for company A should be updated from market_snapshot
        self.assertEqual(result_portfolio.loc[result_portfolio["company"] == "A", "price"].iloc[0], 12)

    def test_sell_empty_portfolio(self):
        # Arrange
        empty_portfolio = pd.DataFrame(columns=["company", "price", "shares", "value"])
        to_sell = {"A", "B"}
        available_funds = float64(100.0)
        
        # Act
        result_portfolio, result_funds = sell(empty_portfolio, self.market_snapshot, to_sell, available_funds)
        
        # Assert
        self.assertTrue(result_portfolio.empty)
        self.assertEqual(result_funds, available_funds)

    def test_sell_nothing_to_sell(self):
        # Arrange
        to_sell = set()
        available_funds = float64(100.0)
        
        # Act
        result_portfolio, result_funds = sell(self.portfolio, self.market_snapshot, to_sell, available_funds)
        
        # Assert
        # Portfolio should be unchanged except for price updates
        self.assertEqual(len(result_portfolio), len(self.portfolio))
        self.assertEqual(result_funds, available_funds)
        # Prices should be updated from market_snapshot
        self.assertEqual(result_portfolio.loc[result_portfolio["company"] == "A", "price"].iloc[0], 12)
        self.assertEqual(result_portfolio.loc[result_portfolio["company"] == "B", "price"].iloc[0], 9)
        self.assertEqual(result_portfolio.loc[result_portfolio["company"] == "C", "price"].iloc[0], 6)

    def test_sell_companies_not_in_portfolio(self):
        # Arrange
        to_sell = {"D", "E"}  # Companies not in portfolio
        available_funds = float64(100.0)
        
        # Act
        result_portfolio, result_funds = sell(self.portfolio, self.market_snapshot, to_sell, available_funds)
        
        # Assert
        # Portfolio should be unchanged except for price updates
        self.assertEqual(len(result_portfolio), len(self.portfolio))
        self.assertEqual(result_funds, available_funds)
        # Companies A, B, C should still be in portfolio
        self.assertTrue("A" in result_portfolio["company"].values)
        self.assertTrue("B" in result_portfolio["company"].values)
        self.assertTrue("C" in result_portfolio["company"].values)

    def test_update_prices_from_market_snapshot(self):
        # Arrange
        to_sell = set()  # Not selling anything, just testing price updates
        available_funds = float64(100.0)
        
        # Act
        result_portfolio, _ = sell(self.portfolio, self.market_snapshot, to_sell, available_funds)
        
        # Assert
        # Check that prices in portfolio are updated from market_snapshot
        self.assertEqual(result_portfolio.loc[result_portfolio["company"] == "A", "price"].iloc[0], 12)
        self.assertEqual(result_portfolio.loc[result_portfolio["company"] == "B", "price"].iloc[0], 9)
        self.assertEqual(result_portfolio.loc[result_portfolio["company"] == "C", "price"].iloc[0], 6)
        # Check that other fields from market_snapshot are transferred
        self.assertEqual(result_portfolio.loc[result_portfolio["company"] == "A", "weight"].iloc[0], 0.4)
        self.assertEqual(result_portfolio.loc[result_portfolio["company"] == "A", "cumulative_weight"].iloc[0], 0.4)

if __name__ == "__main__":
    unittest.main()