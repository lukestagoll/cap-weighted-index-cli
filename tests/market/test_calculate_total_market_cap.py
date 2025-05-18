import unittest
import pandas as pd
from cap_weighted_index_cli.market.calculate_total_market_cap import calculate_total_market_cap

class TestCalculateTotalMarketCap(unittest.TestCase):
    def test_valid_data(self):
        # Arrange
        df = pd.DataFrame({
            "market_cap_m": [
                1000,
                200,
                100,
                50,
            ]
        })
        expected = 1350

        # Act
        actual = calculate_total_market_cap(df)

        # Assert
        self.assertEqual(actual, expected)
        
    def test_empty_rows(self):
        # Arrange
        df = pd.DataFrame({ "market_cap_m": [] })
        expected = 0

        # Act
        actual = calculate_total_market_cap(df)

        # Assert
        self.assertEqual(actual, expected)

    def test_missing_column_raises_keyerror(self):
        df = pd.DataFrame({})
        with self.assertRaises(KeyError) as result:
            calculate_total_market_cap(df)
            
        self.assertIn("`market_cap_m` column not found in `market_data`", str(result.exception))

    def test_invalid_dataframe_raises_typeerror(self):
        with self.assertRaises(TypeError) as result:
            calculate_total_market_cap("not a dataframe") # type: ignore
            
        self.assertIn("`market_data` must be a DataFrame", str(result.exception))

if __name__ == "__main__":
    unittest.main()