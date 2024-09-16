import pandas as pd
import unittest
import datetime

class TestDataValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Read the CSV file using pandas
        cls.df = pd.read_csv('data.csv')
        # Convert columns to appropriate data types
        cls.convert_data_types()

    @classmethod
    def convert_data_types(cls):
        df = cls.df

        # Convert 'date_of_birth' to datetime
        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], format='%Y-%m-%d', errors='coerce')

        # Convert boolean fields
        boolean_fields = [
            'prior_convictions',
            'convicted_against_children',
            'sexual_offender',
            'sexual_predator'
        ]
        for field in boolean_fields:
            df[field] = df[field].astype(str).str.strip().str.lower().map({'true': True, 'false': False})

        # Ensure 'ssn' is treated as a string
        df['ssn'] = df['ssn'].astype(str)

        # Store the cleaned DataFrame
        cls.df = df

    def check_non_empty_string(self, series, field_name):
        """Validate that the Series contains non-empty strings."""
        self.assertFalse(series.isnull().any(), msg=f"Null entries found in '{field_name}'.")
        self.assertFalse(series.str.strip().eq('').any(), msg=f"Empty strings found in '{field_name}'.")

    def check_optional_string(self, series, field_name):
        """Validate that the Series contains strings or is missing (NaN)."""
        # Drop NaN values
        non_null_series = series.dropna()
        # Ensure all non-null entries are strings
        self.assertTrue(non_null_series.apply(lambda x: isinstance(x, str)).all(), msg=f"Non-string entries found in '{field_name}'.")


    def check_single_uppercase_letter(self, series, field_name):
        """Check if each entry is a single uppercase letter."""
        condition = series.str.match(r'^[A-Z]$')
        self.assertTrue(condition.all(), msg=f"Entries in '{field_name}' are not single uppercase letters.")

    def check_comments_length(self, series, field_name, max_words=25):
        """Validate that 'comments' do not exceed a maximum word count."""
        def word_count(text):
            return len(str(text).split()) if pd.notnull(text) else 0
        word_counts = series.apply(word_count)
        invalid_entries = word_counts[word_counts > max_words]
        self.assertTrue(invalid_entries.empty, msg=f"Entries in '{field_name}' exceed {max_words} words.")

    def check_date(self, series, field_name):
        """Validate that dates are valid and not null."""
        invalid_dates = series[series.isnull()]
        self.assertTrue(invalid_dates.empty, msg=f"Invalid dates found in '{field_name}'.")

    def check_age(self, dob_series, field_name, min_age=18, max_age=100):
        """Validate that ages are within the specified range."""
        today = datetime.date.today()
        # Calculate age
        ages = dob_series.apply(lambda dob: today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day)))
        # Check for valid ages
        valid_ages = (ages >= min_age) & (ages <= max_age)
        invalid_ages = ages[~valid_ages]
        self.assertTrue(valid_ages.all(), msg=f"Ages in '{field_name}' are outside {min_age}-{max_age}. Invalid ages: {invalid_ages.values}")

    def check_in_list(self, series, valid_list, field_name):
        """Check if values are within an approved list."""
        invalid_entries = series[~series.isin(valid_list)]
        self.assertTrue(invalid_entries.empty, msg=f"Invalid entries in '{field_name}': {invalid_entries.unique()}")

    def check_boolean(self, series, field_name):
        """Validate that the Series contains only boolean values."""
        valid_booleans = [True, False]
        invalid_entries = series[~series.isin(valid_booleans)]
        self.assertTrue(invalid_entries.empty, msg=f"Invalid boolean values in '{field_name}': {invalid_entries.unique()}")

    def check_unique(self, series, field_name):
        """Ensure that all entries in the Series are unique."""
        duplicates = series[series.duplicated()]
        self.assertTrue(duplicates.empty, msg=f"Duplicate entries in '{field_name}': {duplicates.values}")

    def test_field_validations(self):
        """Perform validations on each field."""
        valid_religions = ["Christianity", "Islam", "Hinduism", "Buddhism", "Other"]
        valid_races = [
            "White",
            "Black or African American",
            "Asian",
            "Hispanic or Latino",
            "Native American",
            "Pacific Islander",
            "Middle Eastern",
            "Mixed Race",
            "Other"
        ]
        valid_genders = ['male', 'female']

        df = self.df

        # Validate 'first_name'
        self.check_non_empty_string(df['first_name'], 'first_name')

        # Validate 'second_name' (middle initial)
        self.check_single_uppercase_letter(df['second_name'], 'second_name')

        # Validate 'last_name'
        self.check_non_empty_string(df['last_name'], 'last_name')

        # Validate 'nickname' (optional string)
        self.check_optional_string(df['nickname'], 'nickname')

        # Validate 'date_of_birth'
        self.check_date(df['date_of_birth'], 'date_of_birth')
        self.check_age(df['date_of_birth'], 'date_of_birth')

        # Validate 'ssn'
        self.check_non_empty_string(df['ssn'], 'ssn')
        self.check_unique(df['ssn'], 'ssn')

        # Validate 'bio_gender'
        self.check_in_list(df['bio_gender'], valid_genders, 'bio_gender')

        # Validate 'religion'
        self.check_in_list(df['religion'], valid_religions, 'religion')

        # Validate 'race'
        self.check_in_list(df['race'], valid_races, 'race')

        # Validate 'language' (non-empty string)
        self.check_non_empty_string(df['language'], 'language')

        # Validate 'voca_classifications' (single uppercase letter)
        self.check_single_uppercase_letter(df['voca_classifications'], 'voca_classifications')

        # Validate 'comments' (optional string with max 15 words)
        self.check_optional_string(df['comments'], 'comments')
        self.check_comments_length(df['comments'], 'comments')

        # Validate boolean fields
        boolean_fields = [
            'prior_convictions',
            'convicted_against_children',
            'sexual_offender',
            'sexual_predator'
        ]
        for field in boolean_fields:
            self.check_boolean(df[field], field)

    def test_all_fields_present(self):
        """Ensure all expected fields are present in the DataFrame."""
        expected_fields = [
            'first_name',
            'second_name',
            'last_name',
            'nickname',
            'date_of_birth',
            'ssn',
            'bio_gender',
            'religion',
            'race',
            'language',
            'voca_classifications',
            'comments',
            'prior_convictions',
            'convicted_against_children',
            'sexual_offender',
            'sexual_predator'
        ]
        missing_fields = set(expected_fields) - set(self.df.columns)
        self.assertTrue(len(missing_fields) == 0, msg=f"Missing fields: {missing_fields}")

if __name__ == '__main__':
    unittest.main()

