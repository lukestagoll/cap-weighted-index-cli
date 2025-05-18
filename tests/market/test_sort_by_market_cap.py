import unittest
import pandas as pd
import pandas.testing as pdt
from cap_weighted_index_cli.market.sort_by_market_cap import sort_by_market_cap

class TestSortByMarketCap(unittest.TestCase):
    def test_unsorted_values(self):
        # Arrange
        df = pd.DataFrame({
            "market_cap_m": [
                100,
                200,
                50,
                1000,
            ]
        })
        expected = pd.DataFrame({
            "market_cap_m": [
                1000,
                200,
                100,
                50,
            ]
        })

        # Act
        actual = sort_by_market_cap(df)

        # Assert
        pdt.assert_frame_equal(actual.reset_index(drop=True), expected)
        
    def test_empty_rows(self):
        # Arrange
        df = pd.DataFrame({ "market_cap_m": [] })
        expected = pd.DataFrame({ "market_cap_m": [] })

        # Act
        actual = sort_by_market_cap(df)

        # Assert
        pdt.assert_frame_equal(actual, expected)

    def test_invalid_column_raises_keyerror(self):
        df = pd.DataFrame({})
        with self.assertRaises(KeyError):
            sort_by_market_cap(df)

if __name__ == "__main__":
    unittest.main()