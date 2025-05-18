import unittest
from numpy import float64
import pandas as pd
import pandas.testing as pdt
from cap_weighted_index_cli.portfolio.identify_portfolio_changes import identify_portfolio_changes

class TestIdentifyPortfolioChanges(unittest.TestCase):
    def test_identify_portfolio_changes(self):
        # Arrange
        portfolio = pd.DataFrame({
            "company": ["A", "B", "C"],
        })
        market_data = pd.DataFrame({
            "company": ["C", "D"],
        })
        expected_to_buy = {"D"}
        expected_to_sell = {"A", "B"}

        # Act
        to_sell, to_buy = identify_portfolio_changes(portfolio, market_data)
        # Assert
        self.assertEqual(to_sell, expected_to_sell)
        self.assertEqual(to_buy, expected_to_buy)

    def test_empty_rows(self):
        # Arrange
        portfolio = pd.DataFrame({
            "company": [],
        })
        market_data = pd.DataFrame({
            "company": [],
        })
        expected_to_buy = set()
        expected_to_sell = set()

        # Act
        to_sell, to_buy = identify_portfolio_changes(portfolio, market_data)
        # Assert
        self.assertEqual(to_sell, expected_to_sell)
        self.assertEqual(to_buy, expected_to_buy)

    def test_portfolio_missing_company_column_raises_keyerror(self):
        portfolio = pd.DataFrame({
        })
        market_data = pd.DataFrame({
            "company": [],
        })
        with self.assertRaises(KeyError) as result:
            identify_portfolio_changes(portfolio, market_data)
            
        self.assertIn("`company` column not found in `portfolio`", str(result.exception))

    def test_filtered_market_data_missing_company_column_raises_keyerror(self):
        portfolio = pd.DataFrame({
            "company": [],
        })
        market_data = pd.DataFrame({
        })
        with self.assertRaises(KeyError) as result:
            identify_portfolio_changes(portfolio, market_data)
            
        self.assertIn("`company` column not found in `filtered_market_data`", str(result.exception))

    def test_invalid_portfolio_dataframe_raises_typeerror(self):
        market_data = pd.DataFrame({
            "company": [],
        })
        with self.assertRaises(TypeError) as result:
            identify_portfolio_changes("not a dataframe", market_data) # type: ignore
            
        self.assertIn("`portfolio` must be a DataFrame", str(result.exception))

    def test_invalid_filtered_market_data_dataframe_raises_typeerror(self):
        portfolio = pd.DataFrame({
            "company": [],
        })
        with self.assertRaises(TypeError) as result:
            identify_portfolio_changes(portfolio, "not a dataframe") # type: ignore
            
        self.assertIn("`filtered_market_data` must be a DataFrame", str(result.exception))

if __name__ == "__main__":
    unittest.main()