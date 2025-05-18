import unittest
import pandas as pd
import pandas.testing as pdt
from cap_weighted_index_cli.market.calculate_total_market_cap import calculate_total_market_cap

class TestSortByMarketCap(unittest.TestCase):
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

    def test_invalid_column_raises_keyerror(self):
        df = pd.DataFrame({})
        with self.assertRaises(KeyError):
            calculate_total_market_cap(df)

if __name__ == "__main__":
    unittest.main()