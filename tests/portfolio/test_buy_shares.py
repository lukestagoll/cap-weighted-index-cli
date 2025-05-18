import unittest
from numpy import float64
import pandas as pd
import pandas.testing as pdt
from cap_weighted_index_cli.portfolio.buy_shares import buy_shares

class TestBuyShares(unittest.TestCase):
    def test_buy_shares(self):
        # Arrange
        portfolio = pd.DataFrame({
            "company": ["A", "B"],
            "price": [10, 8],
            "shares": [4, 3],
            "value": [float64(40), float64(24)],
        })
        shares_to_buy = pd.DataFrame({
            "company": ["C", "D"],
            "price": [1, 2],
            "shares": [5, 6],
        })
        expected_portfolio = pd.DataFrame({
            "company": ["A", "B", "C", "D"],
            "price": [10, 8, 1, 2],
            "shares": [4, 3, 5, 6],
            "value": [float64(40), float64(24), float64(5), float64(12)],
        })
        available_funds = float64(100)
        expected_remaining_funds = float64(83)

        # Act
        new_portfolio, remaining_funds = buy_shares(portfolio, shares_to_buy, available_funds)

        # Assert
        pdt.assert_frame_equal(new_portfolio.reset_index(drop=True), expected_portfolio)
        self.assertEqual(remaining_funds, expected_remaining_funds)

    def test_empty_rows(self):
        # Arrange
        portfolio = pd.DataFrame({
            "company": [],
            "price": [],
            "shares": [],
            "value": [],
        })
        shares_to_buy = pd.DataFrame({
            "company": [],
            "price": [],
            "shares": [],
        })
        expected_portfolio = pd.DataFrame({
            "company": [],
            "price": [],
            "shares": [],
            "value": [],
        })
        available_funds = float64(100)
        
        # Act
        new_portfolio, remaining_funds = buy_shares(portfolio, shares_to_buy, available_funds)

        # Assert
        self.assertEqual(len(new_portfolio["company"]), 0)
        self.assertEqual(remaining_funds, available_funds)

    def test_buy_shares_with_previously_invested_companies_raises_valueerror(self):
        # Arrange
        portfolio = pd.DataFrame({
            "company": ["A", "B"],
            "price": [10, 8],
            "shares": [4, 3],
            "value": [float64(40), float64(24)],
        })
        shares_to_buy = pd.DataFrame({
            "company": ["A", "B"],
            "price": [1, 2],
            "shares": [5, 6],
        })
        available_funds = float64(100)

        # Act
        with self.assertRaises(ValueError) as result:
            buy_shares(portfolio, shares_to_buy, available_funds)
            
        self.assertIn("`shares_to_buy` cannot contain companies that exist in `portfolio`", str(result.exception))

    def test_missing_price_column_raises_keyerror(self):
        portfolio = pd.DataFrame({
            "company": ["A", "B"],
            "price": [10, 8],
            "shares": [4, 3],
            "value": [float64(40), float64(24)],
        })
        shares_to_buy = pd.DataFrame({
            "company": ["C", "D"],
            "shares": [5, 6],
        })
        with self.assertRaises(KeyError) as result:
            buy_shares(portfolio, shares_to_buy, float64(1))
            
        self.assertIn("`price` column not found in `shares_to_buy`", str(result.exception))

    def test_missing_shares_column_raises_keyerror(self):
        portfolio = pd.DataFrame({
            "company": ["A", "B"],
            "price": [10, 8],
            "shares": [4, 3],
            "value": [float64(40), float64(24)],
        })
        shares_to_buy = pd.DataFrame({
            "company": ["C", "D"],
            "price": [1, 2],
        })
        with self.assertRaises(KeyError) as result:
            buy_shares(portfolio, shares_to_buy, float64(1))
            
        self.assertIn("`shares` column not found in `shares_to_buy`", str(result.exception))

    def test_missing_company_column_raises_keyerror(self):
        portfolio = pd.DataFrame({
            "company": ["A", "B"],
            "price": [10, 8],
            "shares": [4, 3],
            "value": [float64(40), float64(24)],
        })
        shares_to_buy = pd.DataFrame({
            "price": [1, 2],
            "shares": [5, 6],
        })
        with self.assertRaises(KeyError) as result:
            buy_shares(portfolio, shares_to_buy, float64(1))
            
        self.assertIn("`company` column not found in `shares_to_buy`", str(result.exception))

    def test_invalid_portfolio_dataframe_raises_typeerror(self):
        shares_to_buy = pd.DataFrame({
            "company": ["A", "B"],
            "price": [1, 2],
            "shares": [5, 6],
        })
        with self.assertRaises(TypeError) as result:
            buy_shares("not a dataframe", shares_to_buy, float64(1)) # type: ignore
            
        self.assertIn("`portfolio` must be a DataFrame", str(result.exception))

    def test_invalid_shares_to_buy_dataframe_raises_typeerror(self):
        portfolio = pd.DataFrame({
            "price": [10, 8],
            "shares": [4, 3],
            "value": [float64(40), float64(24)],
        })
        with self.assertRaises(TypeError) as result:
            buy_shares(portfolio, "not a dataframe", float64(1)) # type: ignore
            
        self.assertIn("`shares_to_buy` must be a DataFrame", str(result.exception))

    def test_invalid_available_funds_raises_typeerror(self):
        portfolio = pd.DataFrame({
            "company": ["A", "B"],
            "price": [10, 8],
            "shares": [4, 3],
            "value": [float64(40), float64(24)],
        })
        shares_to_buy = pd.DataFrame({
            "company": ["C", "D"],
            "price": [1, 2],
            "shares": [5, 6],
        })
        with self.assertRaises(TypeError) as result:
            buy_shares(portfolio, shares_to_buy, 0) # type: ignore
            
        self.assertIn("`available_funds` must be a float64 greater than 0", str(result.exception))

if __name__ == "__main__":
    unittest.main()