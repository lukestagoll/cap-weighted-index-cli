import unittest
from unittest.mock import patch, MagicMock
import sys
import click
from click.testing import CliRunner
from numpy import float64
from cap_weighted_index_cli.cli import main

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        
    @patch('cap_weighted_index_cli.cli.parse_csv')
    @patch('cap_weighted_index_cli.cli.trade')
    def test_main_with_default_options(self, mock_trade, mock_parse_csv):
        # Arrange
        mock_market_data = MagicMock()
        mock_parse_csv.return_value = mock_market_data
        
        # Act
        result = self.runner.invoke(main, [])
        
        # Assert
        self.assertEqual(result.exit_code, 0)
        mock_parse_csv.assert_called_once_with("data/input/market_capitalisation.csv")
        mock_trade.assert_called_once()
        # Verify trade was called with correct parameters
        args, kwargs = mock_trade.call_args
        self.assertEqual(args[0], mock_market_data)
        self.assertEqual(type(args[1]), float64)
        self.assertEqual(type(args[2]), float64)
        self.assertEqual(args[1], float64(100000000.00))
        self.assertEqual(args[2], float64(0.85))

    @patch('cap_weighted_index_cli.cli.parse_csv')
    @patch('cap_weighted_index_cli.cli.trade')
    def test_main_with_custom_options(self, mock_trade, mock_parse_csv):
        # Arrange
        mock_market_data = MagicMock()
        mock_parse_csv.return_value = mock_market_data
        
        # Act
        result = self.runner.invoke(main, [
            "--available-funds", "50000",
            "--max-cumulative-weight", "0.75"
        ])
        print(result)
        # Assert
        self.assertEqual(result.exit_code, 0)
        mock_trade.assert_called_once()
        # Verify trade was called with custom parameters
        args, kwargs = mock_trade.call_args
        self.assertEqual(args[0], mock_market_data)
        self.assertEqual(args[1], float64(50000))
        self.assertEqual(args[2], float64(0.75))

    @patch('cap_weighted_index_cli.cli.parse_csv')
    def test_main_with_invalid_csv(self, mock_parse_csv):
        # Arrange
        mock_parse_csv.return_value = None
        
        # Act
        result = self.runner.invoke(main, [])
        
        # Assert
        self.assertEqual(result.exit_code, 1)
        mock_parse_csv.assert_called_once()
        # Trade should not be called if CSV parsing fails

    @patch('cap_weighted_index_cli.cli.parse_csv')
    @patch('cap_weighted_index_cli.cli.trade')
    def test_main_with_trade_value_error(self, mock_trade, mock_parse_csv):
        # Arrange
        mock_market_data = MagicMock()
        mock_parse_csv.return_value = mock_market_data
        mock_trade.side_effect = ValueError("Test error")
        
        # Act
        result = self.runner.invoke(main, [])
        
        # Assert
        self.assertEqual(result.exit_code, 1)
        mock_parse_csv.assert_called_once()
        mock_trade.assert_called_once()
        # Error should be logged and program should exit with code 1

    def test_validate_max_cumulative_weight_range(self):
        # Test with a value outside the allowed range (> 0.85)
        result = self.runner.invoke(main, ["--max-cumulative-weight", "0.95"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Invalid value", result.output)
        
        # Test with a value at the lower boundary (0.0)
        result = self.runner.invoke(main, ["--max-cumulative-weight", "0.0"])
        self.assertEqual(result.exit_code, 0)
        
        # Test with a value at the upper boundary (0.85)
        result = self.runner.invoke(main, ["--max-cumulative-weight", "0.85"])
        self.assertEqual(result.exit_code, 0)

    def test_help_output(self):
        # Test the help output contains all options
        result = self.runner.invoke(main, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("--input", result.output)
        self.assertIn("--available-funds", result.output)
        self.assertIn("--max-cumulative-weight", result.output)
        self.assertIn("Market Cap Index", result.output)

    @patch('cap_weighted_index_cli.cli.parse_csv')
    @patch('cap_weighted_index_cli.cli.get_console')
    @patch('cap_weighted_index_cli.cli.trade')
    def test_console_output(self, mock_trade, mock_get_console, mock_parse_csv):
        # Arrange
        mock_console = MagicMock()
        mock_get_console.return_value = mock_console
        import pandas as pd
        mock_market_data = pd.DataFrame()
        mock_parse_csv.return_value = mock_market_data
        
        # Act
        result = self.runner.invoke(main, [])
        # Assert
        self.assertEqual(result.exit_code, 0)
        # Verify expected console output sequence
        mock_console.print.assert_any_call("Reading Market Data From: 'data/input/market_capitalisation.csv'")
        mock_console.print.assert_any_call("Processing...")

    def test_input_file_not_exists(self):
        # Test behavior when input file doesn't exist
        result = self.runner.invoke(main, ["--input", "nonexistent.csv"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("does not exist", result.output)

if __name__ == "__main__":
    unittest.main()