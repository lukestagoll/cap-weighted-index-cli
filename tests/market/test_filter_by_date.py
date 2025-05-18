import unittest
import pandas as pd
from cap_weighted_index_cli.market.filter_by_date import filter_by_date

class TestFilterByDate(unittest.TestCase):
    def test_filter_by_date_string(self):
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

    def test_filter_by_timestamp(self):
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
        result = filter_by_date(df, pd.Timestamp("01/02/2025"))

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

    def test_missing_column_raises_keyerror(self):
        df = pd.DataFrame({})
        with self.assertRaises(KeyError) as result:
            filter_by_date(df, "01/04/2025")
            
        self.assertIn("`date` column not found in `market_data`", str(result.exception))

    def test_invalid_dataframe_raises_typeerror(self):
        with self.assertRaises(TypeError) as result:
            filter_by_date("not a dataframe", "01/04/2025") # type: ignore
            
        self.assertIn("`market_data` must be a DataFrame", str(result.exception))

    def test_invalid_date_raises_typeerror(self):
        df = pd.DataFrame({ "date": [] })
        with self.assertRaises(TypeError) as result:
            filter_by_date(df, "invalid date") # type: ignore
            
        self.assertIn("`date` must be a Timestamp or a date string in the format \"DD/MM/YYYY\"", str(result.exception))

if __name__ == "__main__":
    unittest.main()