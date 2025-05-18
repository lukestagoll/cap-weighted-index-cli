import unittest
from numpy import float64
import pandas as pd
import pandas.testing as pdt
from cap_weighted_index_cli.portfolio.sell_shares import sell_shares

class TestSellShares(unittest.TestCase):
    def test_sell_shares(self):
        # Arrange
        df = pd.DataFrame({
            "price": [10, 8],
            "shares": [4, 3],
        })
        expected_df = pd.DataFrame({
            "price": [10, 8],
            "shares": [4, 3],
            "value": [float64(40), float64(24)],
        })
        available_funds = float64(100)
        expected_remaining_funds = float64(164)

        # Act
        actual_df, remaining_funds = sell_shares(df, available_funds)

        # Assert
        pdt.assert_frame_equal(actual_df.reset_index(drop=True), expected_df)
        self.assertEqual(remaining_funds, expected_remaining_funds)

    def test_empty_rows(self):
        # Arrange
        df = pd.DataFrame({ "price": [], "shares": [] })
        available_funds = float64(100)
        
        # Act
        actual_df, remaining_funds = sell_shares(df, available_funds)

        # Assert
        self.assertEqual(len(actual_df["value"]), 0)
        self.assertEqual(remaining_funds, available_funds)

    def test_missing_price_column_raises_keyerror(self):
        df = pd.DataFrame({ "shares": [] })
        with self.assertRaises(KeyError) as result:
            sell_shares(df, float64(1))
            
        self.assertIn("`price` column not found in `shares_to_sell`", str(result.exception))

    def test_missing_weight_column_raises_keyerror(self):
        df = pd.DataFrame({ "price": [] })
        with self.assertRaises(KeyError) as result:
            sell_shares(df, float64(1))
            
        self.assertIn("`shares` column not found in `shares_to_sell`", str(result.exception))

    def test_invalid_dataframe_raises_typeerror(self):
        with self.assertRaises(TypeError) as result:
            sell_shares("not a dataframe", float64(1)) # type: ignore
            
        self.assertIn("`shares_to_sell` must be a DataFrame", str(result.exception))

    def test_invalid_available_funds_raises_typeerror(self):
        df = pd.DataFrame({ "price": [], "weight": [] })
        with self.assertRaises(TypeError) as result:
            sell_shares(df, -1) # type: ignore
            
        self.assertIn("`available_funds` must be a float64 greater than or equal to 0", str(result.exception))

if __name__ == "__main__":
    unittest.main()