import unittest
from numpy import float64
import pandas as pd
import pandas.testing as pdt
from cap_weighted_index_cli.market.filter_by_cumulative_weight import filter_by_cumulative_weight

class TestCalculateCumulativeWeights(unittest.TestCase):
    def test_filter_by_cumulative_weight(self):
        # Arrange
        df = pd.DataFrame({
            "cumulative_weight": [0.4, 0.7, 0.9, 1.0]
        })
        expected = pd.DataFrame({
            "cumulative_weight": [0.4, 0.7, 0.9]
        })

        # Act
        actual = filter_by_cumulative_weight(df, float64(0.9))

        # Assert
        pdt.assert_frame_equal(actual.reset_index(drop=True), expected)

    def test_empty_rows(self):
        # Arrange
        df = pd.DataFrame({ "cumulative_weight": [] })
        expected = pd.DataFrame({ "cumulative_weight": [] })

        # Act
        actual = filter_by_cumulative_weight(df, float64(0))

        # Assert
        pdt.assert_frame_equal(actual, expected)

    def test_invalid_max_cumulative_weight_raises_typeerror(self):
        df = pd.DataFrame({
            "cumulative_weight": [0.4, 0.7, 0.9, 1.0]
        })
        with self.assertRaises(TypeError) as result:
            filter_by_cumulative_weight(df, "1") # type: ignore
            
        self.assertIn("`max_cumulative_weight` must be a float64", str(result.exception))

    def test_missing_column_raises_keyerror(self):
        df = pd.DataFrame({})
        with self.assertRaises(KeyError) as result:
            filter_by_cumulative_weight(df, float64(0.5))
            
        self.assertIn("`cumulative_weight` column not found in `market_data`", str(result.exception))

    def test_invalid_dataframe_raises_typeerror(self):
        with self.assertRaises(TypeError) as result:
            filter_by_cumulative_weight("not a dataframe", float64(0.5)) # type: ignore
            
        self.assertIn("`market_data` must be a DataFrame", str(result.exception))

if __name__ == "__main__":
    unittest.main()