import unittest
import pandas as pd
from datetime import datetime
from cap_weighted_index_cli.data.get_dates import get_dates

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

    def test_missing_date_column_raises_key_error(self):
        # Arrange
        df = pd.DataFrame({})

        # Act & Assert
        with self.assertRaises(KeyError):
            get_dates(df)

if __name__ == "__main__":
    unittest.main()