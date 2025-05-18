import unittest
from click.testing import CliRunner
from cap_weighted_index_cli.cli import main

class CLITest(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_main_command(self):
        # Test the main command
        result = self.runner.invoke(main, [])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Reading from", result.output)
        
    def test_help_output(self):
        # Test the help output
        result = self.runner.invoke(main, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Market Cap Index", result.output)

if __name__ == "__main__":
    unittest.main()
