import unittest
from numpy import float64
import pandas as pd
import pandas.testing as pdt
from cap_weighted_index_cli.portfolio.calculate_shares_to_buy import calculate_shares_to_buy

class TestCalculateSharesToBuy(unittest.TestCase):
    def test_calculate_shares_to_buy(self):
        # Arrange
        df = pd.DataFrame({
            "price": [10, 8],
            "weight": [0.4, 0.3],
        })
        expected = pd.DataFrame({
            "price": [10, 8],
            "weight": [0.4, 0.3],
            "shares": [4, 3],
        })
        available_funds = float64(100)

        # Act
        actual = calculate_shares_to_buy(df, available_funds)

        # Assert
        pdt.assert_frame_equal(actual.reset_index(drop=True), expected)

    def test_calculate_shares_to_buy_with_existing_values(self):
        # Arrange
        df = pd.DataFrame({
            "price": [10, 8],
            "weight": [0.4, 0.3],
            "shares": [0, 0],
        })
        expected = pd.DataFrame({
            "price": [10, 8],
            "weight": [0.4, 0.3],
            "shares": [4, 3],
        })
        available_funds = float64(100)

        # Act
        actual = calculate_shares_to_buy(df, available_funds)

        # Assert
        pdt.assert_frame_equal(actual.reset_index(drop=True), expected)
        
    def test_empty_rows(self):
        # Arrange
        df = pd.DataFrame({ "price": [], "weight": [] })
        expected = pd.DataFrame({ "price": [], "weight": [], "shares": [] })
        available_funds = float64(100)
        
        # Act
        actual = calculate_shares_to_buy(df, available_funds)

        # Assert
        self.assertEqual(len(actual["shares"]), 0)

    def test_missing_price_column_raises_keyerror(self):
        df = pd.DataFrame({ "weight": [] })
        with self.assertRaises(KeyError) as result:
            calculate_shares_to_buy(df, float64(1))
            
        self.assertIn("`price` column not found in `portfolio`", str(result.exception))

    def test_missing_weight_column_raises_keyerror(self):
        df = pd.DataFrame({ "price": [] })
        with self.assertRaises(KeyError) as result:
            calculate_shares_to_buy(df, float64(1))
            
        self.assertIn("`weight` column not found in `portfolio`", str(result.exception))

    def test_invalid_dataframe_raises_typeerror(self):
        with self.assertRaises(TypeError) as result:
            calculate_shares_to_buy("not a dataframe", 1) # type: ignore
            
        self.assertIn("`portfolio` must be a DataFrame", str(result.exception))

    def test_invalid_available_funds_raises_typeerror(self):
        df = pd.DataFrame({ "price": [], "weight": [] })
        with self.assertRaises(TypeError) as result:
            calculate_shares_to_buy(df, 0) # type: ignore
            
        self.assertIn("`available_funds` must be a float64 greater than 0", str(result.exception))

if __name__ == "__main__":
    unittest.main()