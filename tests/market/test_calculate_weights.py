import unittest
import pandas as pd
import numpy as np
import pandas.testing as pdt
from cap_weighted_index_cli.market.calculate_weights import calculate_weights

class TestCalculateWeights(unittest.TestCase):
    def test_calculate_weights(self):
        # Arrange
        df = pd.DataFrame({
            "market_cap_m": [1000, 200, 100, 50]
        })
        total_market_cap = 1350
        expected = pd.DataFrame({
            "market_cap_m": [1000, 200, 100, 50],
            "weight": [
                np.float64(1000 / 1350),
                np.float64(200 / 1350),
                np.float64(100 / 1350),
                np.float64(50 / 1350),
            ]
        })

        # Act
        actual = calculate_weights(df, total_market_cap)

        # Assert
        pdt.assert_frame_equal(actual.reset_index(drop=True), expected)

    def test_calculate_weights_with_existing_values(self):
        # Arrange
        df = pd.DataFrame({
            "market_cap_m": [1000, 200, 100, 50],
            "weight": [0, 0, 0, 0]
        })
        total_market_cap = 1350
        expected = pd.DataFrame({
            "market_cap_m": [1000, 200, 100, 50],
            "weight": [
                np.float64(1000 / 1350),
                np.float64(200 / 1350),
                np.float64(100 / 1350),
                np.float64(50 / 1350),
            ]
        })

        # Act
        actual = calculate_weights(df, total_market_cap)

        # Assert
        pdt.assert_frame_equal(actual.reset_index(drop=True), expected)
        
    def test_empty_rows(self):
        # Arrange
        df = pd.DataFrame({ "market_cap_m": [] })
        expected = pd.DataFrame({ "market_cap_m": [], "weight": [] })

        # Act
        actual = calculate_weights(df, 0)

        # Assert
        pdt.assert_frame_equal(actual, expected)

    def test_invalid_column_raises_keyerror(self):
        df = pd.DataFrame({})
        with self.assertRaises(KeyError):
            calculate_weights(df, 0)

if __name__ == "__main__":
    unittest.main()