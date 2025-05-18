import unittest
import pandas as pd
from cap_weighted_index_cli.market.filter_by_date import filter_by_date

class TestFilterByDate(unittest.TestCase):
    def test_sorted_unique_dates(self):
        # Arrange
        df = pd.DataFrame({
            "date": [
                pd.Timestamp("01/01/2025"),
                pd.Timestamp("01/01/2025"),
                pd.Timestamp("01/02/2025"),
                pd.Timestamp("01/02/2025"),
                pd.Timestamp("01/02/2025"),
                pd.Timestamp("01/03/2025"),
                pd.Timestamp("01/03/2025"),
            ]
        })

        # Act
        result = filter_by_date(df, "01/02/2025")

        # Assert
        self.assertEqual(len(result), 3)
        self.assertTrue((result["date"] == pd.Timestamp("01/02/2025")).all())

    def test_filter_no_matches(self):
        df = pd.DataFrame({
            "date": [
                pd.Timestamp("01/01/2025"),
                pd.Timestamp("01/01/2025"),
                pd.Timestamp("01/02/2025"),
                pd.Timestamp("01/02/2025"),
                pd.Timestamp("01/02/2025"),
                pd.Timestamp("01/03/2025"),
                pd.Timestamp("01/03/2025"),
            ]
        })
        result = filter_by_date(df, "01/04/2025")
        self.assertTrue(result.empty)

    def test_invalid_column_raises_keyerror(self):
        df = pd.DataFrame({})
        with self.assertRaises(KeyError):
            filter_by_date(df, "01/02/2025")

if __name__ == "__main__":
    unittest.main()