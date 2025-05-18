import unittest
from unittest.mock import patch, MagicMock
from numpy import float64
import pandas as pd
import pandas.testing as pdt
from cap_weighted_index_cli.execution.buy import buy

class TestBuy(unittest.TestCase):
    def setUp(self):
        # Setup initial test data
        self.portfolio = pd.DataFrame({
            "company": ["A", "B"],
            "market_cap_m": [100, 50],
            "price": [10, 8],
            "weight": [0.4, 0.3],
            "cumulative_weight": [0.4, 0.7],
            "shares": [4, 3],
            "value": [float64(40), float64(24)],
        })
        
        self.market_snapshot = pd.DataFrame({
            "company": ["A", "B", "C", "D"],
            "price": [10, 8, 5, 2],
            "weight": [0.4, 0.3, 0.2, 0.1],
            "market_cap_m": [400, 300, 200, 100],
            "cumulative_weight": [0.4, 0.7, 0.9, 1.0],
        })

    @patch('cap_weighted_index_cli.execution.buy.calculate_shares_to_buy')
    @patch('cap_weighted_index_cli.execution.buy.buy_shares')
    def test_buy_normal_execution(self, mock_buy_shares, mock_calculate_shares_to_buy):
        # Arrange
        to_buy = {"C", "D"}
        available_funds = float64(100.0)
        
        mock_shares_to_buy = pd.DataFrame({
            "company": ["C", "D"],
            "price": [5, 2],
            "shares": [4, 5],
            "weight": [0.2, 0.1]
        })
        
        expected_portfolio = pd.DataFrame({
            "company": ["A", "B", "C", "D"],
            "price": [10, 8, 5, 2],
            "shares": [4, 3, 4, 5],
            "value": [float64(40), float64(24), float64(20), float64(10)]
        })
        expected_funds = float64(70.0)
        
        mock_calculate_shares_to_buy.return_value = mock_shares_to_buy
        mock_buy_shares.return_value = (expected_portfolio, expected_funds)
        
        # Act
        result_portfolio, result_funds = buy(self.portfolio, self.market_snapshot, to_buy, available_funds)
        
        # Assert
        self.assertEqual(mock_calculate_shares_to_buy.call_count, 1)
        self.assertEqual(mock_buy_shares.call_count, 1)
        pdt.assert_frame_equal(result_portfolio, expected_portfolio)
        self.assertEqual(result_funds, expected_funds)

    def test_buy_integration(self):
        # Arrange
        to_buy = {"C", "D"}
        available_funds = float64(100.0)
        
        # Act
        result_portfolio, result_funds = buy(self.portfolio, self.market_snapshot, to_buy, available_funds)
        
        # Assert
        # Check companies C and D were added
        self.assertTrue("C" in result_portfolio["company"].values)
        self.assertTrue("D" in result_portfolio["company"].values)
        self.assertGreater(len(result_portfolio), len(self.portfolio))
        self.assertLess(float(result_funds), float(available_funds))

    def test_buy_empty_portfolio(self):
        # Arrange
        empty_portfolio = pd.DataFrame(columns=["company", "price", "shares", "value"])
        to_buy = {"A", "B"}
        available_funds = float64(100.0)
        
        # Act
        result_portfolio, result_funds = buy(empty_portfolio, self.market_snapshot, to_buy, available_funds)
        
        # Assert
        self.assertGreater(len(result_portfolio), 0)
        self.assertTrue("A" in result_portfolio["company"].values)
        self.assertTrue("B" in result_portfolio["company"].values)
        self.assertLess(float(result_funds), float(available_funds))

    def test_buy_no_companies_to_buy(self):
        # Arrange
        to_buy = set()
        available_funds = float64(100.0)
        
        # Act
        result_portfolio, result_funds = buy(self.portfolio, self.market_snapshot, to_buy, available_funds)
        print(result_portfolio, self.portfolio)
        # Assert
        pdt.assert_frame_equal(result_portfolio, self.portfolio)
        self.assertEqual(result_funds, available_funds)

    def test_buy_companies_not_in_market_snapshot(self):
        # Arrange
        to_buy = {"E", "F"}  # Companies not in market_snapshot
        available_funds = float64(100.0)
        
        # Act
        result_portfolio, result_funds = buy(self.portfolio, self.market_snapshot, to_buy, available_funds)
        
        # Assert
        # Should return original portfolio and funds unchanged
        pdt.assert_frame_equal(result_portfolio, self.portfolio)
        self.assertEqual(result_funds, available_funds)

if __name__ == "__main__":
    unittest.main()