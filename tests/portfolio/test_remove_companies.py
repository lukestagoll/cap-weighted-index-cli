import unittest
from numpy import float64
import pandas as pd
import pandas.testing as pdt
from cap_weighted_index_cli.portfolio.remove_companies import remove_companies

class TestRemoveCompanies(unittest.TestCase):
    def test_remove_companies(self):
        # Arrange
        df = pd.DataFrame({ "company": ["A", "B", "C", "D"] })
        companies = { "B", "D" }

        expected_df = pd.DataFrame({ "company": ["A", "C"] })

        # Act
        actual_df = remove_companies(df, companies)

        # Assert
        pdt.assert_frame_equal(actual_df.reset_index(drop=True), expected_df)

    def test_empty_rows(self):
        # Arrange
        df = pd.DataFrame({ "company": [] })
        companies = { "B", "D" }
        
        # Act
        actual_df = remove_companies(df, companies)

        # Assert
        self.assertEqual(len(actual_df["company"]), 0)

    def test_invalid_set_raises_typeerror(self):
        df = pd.DataFrame({ "company": [] })
        companies = ""
        with self.assertRaises(TypeError) as result:
            remove_companies(df, companies) # type: ignore
            
        self.assertIn("`companies` must be a set of strings", str(result.exception))
        
    def test_set_with_invalid_values_raises_typeerror(self):
        df = pd.DataFrame({ "company": [] })
        companies = { 1, 2 }
        with self.assertRaises(TypeError) as result:
            remove_companies(df, companies) # type: ignore
            
        self.assertIn("`companies` must be a set of strings", str(result.exception))

    def test_missing_company_column_raises_keyerror(self):
        df = pd.DataFrame({})
        companies = { "B", "D" }
        with self.assertRaises(KeyError) as result:
            remove_companies(df, companies)
            
        self.assertIn("`company` column not found in `portfolio`", str(result.exception))

    def test_invalid_dataframe_raises_typeerror(self):
        companies = { "B", "D" }
        with self.assertRaises(TypeError) as result:
            remove_companies("not a dataframe", companies) # type: ignore
            
        self.assertIn("`portfolio` must be a DataFrame", str(result.exception))

if __name__ == "__main__":
    unittest.main()