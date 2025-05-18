import unittest
import pandas as pd
from cap_weighted_index_cli.market.get_dates import get_dates

class TestGetDates(unittest.TestCase):
    def test_sorted_unique_dates(self):
        # Arrange
        df = pd.DataFrame({
            "date": [
                pd.Timestamp("01/03/2025"),
                pd.Timestamp("01/01/2025"),
                pd.Timestamp("01/02/2025"),
            ]
        })
        expected = [
            pd.Timestamp("01/01/2025"),
            pd.Timestamp("01/02/2025"),
            pd.Timestamp("01/03/2025"),
        ]

        # Act
        result = get_dates(df)

        # Assert
        self.assertEqual(result, expected)

    def test_empty_dataframe(self):
        # Arrange
        df = pd.DataFrame({"date": []})

        # Act
        result = get_dates(df)
        
        # Assert
        self.assertEqual(result, [])

    def test_dates_with_duplicates(self):
        # Arrange
        df = pd.DataFrame({"date": ["01/02/2025", "01/01/2025", "01/01/2025"]})
        df["date"] = pd.to_datetime(df["date"])

        expected = [
            pd.Timestamp("01/01/2025"),
            pd.Timestamp("01/02/2025"),
        ]

        # Act
        result = get_dates(df)

        # Assert
        self.assertEqual(result, expected)

    def test_missing_column_raises_keyerror(self):
        df = pd.DataFrame({})
        with self.assertRaises(KeyError) as result:
            get_dates(df)
            
        self.assertIn("`date` column not found in `market_data`", str(result.exception))

    def test_invalid_dataframe_raises_typeerror(self):
        with self.assertRaises(TypeError) as result:
            get_dates("not a dataframe") # type: ignore
            
        self.assertIn("`market_data` must be a DataFrame", str(result.exception))

if __name__ == "__main__":
    unittest.main()