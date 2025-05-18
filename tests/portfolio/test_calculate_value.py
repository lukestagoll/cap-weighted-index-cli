import unittest
from numpy import float64
import pandas as pd
import pandas.testing as pdt
from cap_weighted_index_cli.portfolio.calculate_value import calculate_value

class TestCalculateValue(unittest.TestCase):
    def test_calculate_value(self):
        # Arrange
        portfolio = pd.DataFrame({
            "value": [float64(40), float64(24)],
        })
        available_funds = float64(100)
        expected_value = float64(164)

        # Act
        value = calculate_value(portfolio, available_funds)
        # Assert
        self.assertEqual(value, expected_value)

    def test_empty_rows(self):
        # Arrange
        portfolio = pd.DataFrame({
            "value": [],
        })
        available_funds = float64(100)
        
        # Act
        value = calculate_value(portfolio, available_funds)

        # Assert
        self.assertEqual(value, available_funds)

    def test_missing_value_column_raises_keyerror(self):
        portfolio = pd.DataFrame({})

        with self.assertRaises(KeyError) as result:
            calculate_value(portfolio, float64(1))
            
        self.assertIn("`value` column not found in `portfolio`", str(result.exception))

    def test_invalid_portfolio_dataframe_raises_typeerror(self):
        with self.assertRaises(TypeError) as result:
            calculate_value("not a dataframe", float64(1)) # type: ignore
            
        self.assertIn("`portfolio` must be a DataFrame", str(result.exception))

    def test_invalid_available_funds_raises_typeerror(self):
        portfolio = pd.DataFrame({
            "value": [float64(40), float64(24)],
        })
        with self.assertRaises(TypeError) as result:
            calculate_value(portfolio, -1) # type: ignore
            
        self.assertIn("`available_funds` must be a float64 greater than or equal to 0", str(result.exception))

if __name__ == "__main__":
    unittest.main()