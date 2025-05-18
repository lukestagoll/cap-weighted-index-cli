import unittest
import pandas as pd
import pandas.testing as pdt
from cap_weighted_index_cli.analysis.calculate_cumulative_weights import calculate_cumulative_weights

class TestCalculateCumulativeWeights(unittest.TestCase):
    def test_calculate_cumulative_weights(self):
        # Arrange
        df = pd.DataFrame({
            "weight": [0.4, 0.3, 0.2, 0.1]
        })
        expected = pd.DataFrame({
            "weight": [0.4, 0.3, 0.2, 0.1],
            "cumulative_weight": [0.4, 0.7, 0.9, 1.0]
        })

        # Act
        actual = calculate_cumulative_weights(df)

        # Assert
        pdt.assert_frame_equal(actual.reset_index(drop=True), expected)

    def test_calculate_cumulative_weights_with_existing_values(self):
        # Arrange
        df = pd.DataFrame({
            "weight": [0.4, 0.3, 0.2, 0.1],
            "cumulative_weight": [0.2, 0.6, 0.4, 1.0]
        })
        expected = pd.DataFrame({
            "weight": [0.4, 0.3, 0.2, 0.1],
            "cumulative_weight": [0.4, 0.7, 0.9, 1.0]
        })

        # Act
        actual = calculate_cumulative_weights(df)

        # Assert
        pdt.assert_frame_equal(actual.reset_index(drop=True), expected)
        
    def test_empty_rows(self):
        # Arrange
        df = pd.DataFrame({ "weight": [] })
        expected = pd.DataFrame({ "weight": [], "cumulative_weight": [] })

        # Act
        actual = calculate_cumulative_weights(df)

        # Assert
        pdt.assert_frame_equal(actual, expected)

    def test_missing_column_raises_keyerror(self):
        df = pd.DataFrame({})
        with self.assertRaises(KeyError) as result:
            calculate_cumulative_weights(df)
            
        self.assertIn("`weight` column not found in `market_data`", str(result.exception))

    def test_invalid_dataframe_raises_typeerror(self):
        with self.assertRaises(TypeError) as result:
            calculate_cumulative_weights("not a dataframe") # type: ignore
            
        self.assertIn("`market_data` must be a DataFrame", str(result.exception))

if __name__ == "__main__":
    unittest.main()