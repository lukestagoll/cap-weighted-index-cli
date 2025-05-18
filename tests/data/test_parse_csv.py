import unittest
import pandas as pd
from unittest.mock import patch
from cap_weighted_index_cli.data.parse_csv import parse_csv

class TestParseCSV(unittest.TestCase):
    @patch("pandas.read_csv")
    def test_valid_csv(self, mock_read_csv):
        # Arrange
        valid_data = {
            "date": ["2025-01-01", "2025-01-01", "2025-01-01"],
            "company": ["A", "B", "C"],
            "market_cap_m": [2500, 200, 1800],
            "price": [15.25, 3.50, 20.75]
        }
        mock_df = pd.DataFrame(valid_data)
        mock_read_csv.return_value = mock_df

        # Act
        validated_df = parse_csv("dummy.csv")
        
        # Assert
        self.assertIsNotNone(validated_df)
        self.assertTrue(isinstance(validated_df, pd.DataFrame))

        if validated_df is None:
            return
        self.assertListEqual(list(validated_df), ["date", "company", "market_cap_m", "price"])

    @patch("pandas.read_csv")
    def test_csv_invalid_date(self, mock_read_csv):
        # Arrange
        invalid_data = {
            "date": ["A", "B", "C"],
            "company": ["A", "B", "C"],
            "market_cap_m": [2500, 200, 1800],
            "price": [15.25, 3.50, 20.75]
        }
        mock_df = pd.DataFrame(invalid_data)
        mock_read_csv.return_value = mock_df

        # Act
        with self.assertLogs(level="ERROR") as log_output:
            validated_df = parse_csv("dummy.csv")

        # Assert
        self.assertIsNone(validated_df)
        log_text = log_text = "\n".join(log_output.output)
        self.assertIn("CSV format is invalid", log_text)

    @patch("pandas.read_csv")
    def test_csv_invalid_market_cap_m(self, mock_read_csv):
        # Arrange
        invalid_data = {
            "date": ["2025-01-01", "2025-01-01", "2025-01-01"],
            "company": ["A", "B", "C"],
            "market_cap_m": [-1, 200, 1800],
            "price": [15.25, 3.50, 20.75]
        }
        mock_df = pd.DataFrame(invalid_data)
        mock_read_csv.return_value = mock_df

        # Act
        with self.assertLogs(level="ERROR") as log_output:
            validated_df = parse_csv("dummy.csv")

        # Assert
        self.assertIsNone(validated_df)
        log_text = log_text = "\n".join(log_output.output)
        self.assertIn("CSV format is invalid", log_text)

    @patch("pandas.read_csv")
    def test_csv_invalid_price(self, mock_read_csv):
        # Arrange
        invalid_data = {
            "date": ["2025-01-01", "2025-01-01", "2025-01-01"],
            "company": ["A", "B", "C"],
            "market_cap_m": [2500, 200, 1800],
            "price": [-15.25, 3.50, 20.75]
        }
        mock_df = pd.DataFrame(invalid_data)
        mock_read_csv.return_value = mock_df

        # Act
        with self.assertLogs(level="ERROR") as log_output:
            validated_df = parse_csv("dummy.csv")

        # Assert
        self.assertIsNone(validated_df)
        log_text = log_text = "\n".join(log_output.output)
        self.assertIn("CSV format is invalid", log_text)

if __name__ == "__main__":
    unittest.main()
