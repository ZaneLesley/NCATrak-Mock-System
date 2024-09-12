import pandas as pd
import unittest
import datetime

class TestDataValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load the data once before all tests
        cls.df = pd.read_csv('data.csv')

    def check_non_empty_string(self, series, field_name):
        """ Validate non-empty strings in a given Series. """
        self.assertFalse(series.str.strip().eq('').any(), msg=f"Some entries in {field_name} are empty.")

    def check_optional_string(self, series, field_name):
        """ Validate strings, allowing them to be empty. """
        self.assertTrue(pd.api.types.is_string_dtype(series), msg=f"{field_name} must contain only string data.")

    def check_single_uppercase_letter(self, series, field_name):
        """ Check if the Series contains single uppercase letters. """
        condition = (series.str.isupper() & series.str.len().eq(1))
        self.assertTrue(condition.all(), msg=f"Not all entries in {field_name} are single uppercase letters.")

    def check_comments_length(self, comments_series, field_name, max_words=15):
        """ Validate the length of comments based on word count, allowing for empty comments. """
        def word_count(text):
            return len(text.split()) if text.strip() != '' else 0

        word_counts = comments_series.apply(word_count)
        valid_comments = (word_counts <= max_words)
        self.assertTrue(valid_comments.all(), msg=f"Some entries in {field_name} exceed the maximum word count of {max_words}.")

    def check_date(self, series, field_name):
        """ Validate dates. """
        try:
            pd.to_datetime(series, errors='raise')
        except Exception as e:
            self.fail(msg=f"Date conversion error in {field_name}: {str(e)}")

    def check_age(self, dob_series, field_name, min_age=18, max_age=100):
        today = datetime.date.today()
        # Calculate age by subtracting the birth year from the current year and adjusting for the birth date
        ages = dob_series.apply(lambda dob: today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day)))
        valid_ages = (ages >= min_age) & (ages <= max_age)
        self.assertTrue(valid_ages.all(), msg=f"Ages in {field_name} are outside the allowed range of {min_age} to {max_age}.")

    def check_in_list(self, series, valid_list, field_name):
        """ Check if values are in an approved list. """
        self.assertTrue(series.isin(valid_list).all(), msg=f"Some entries in {field_name} are not in the approved list: {set(series) - set(valid_list)}")

    def check_boolean(self, series, field_name):
        """ Validate boolean fields. """
        self.assertTrue(pd.api.types.is_bool_dtype(series), msg=f"{field_name} must contain only boolean values.")

    def check_unique(self, series, field_name):
        """ Ensure all entries in a series are unique. """
        self.assertFalse(series.duplicated().any(), msg=f"There are duplicates in {field_name}.")

    def test_field_validations(self):
        valid_religions = ["Christianity", "Islam", "Hinduism", "Buddhism", "Other"]
        valid_races = ["White", "Black or African American", "Asian", "Hispanic or Latino", "Native American", "Pacific Islander", "Middle Eastern", "Mixed Race", "Other"]
        valid_genders = ['male', 'female']

        self.check_non_empty_string(TestDataValidation.df['first_name'], 'first_name')
        self.check_non_empty_string(TestDataValidation.df['last_name'], 'last_name')
        self.check_single_uppercase_letter(TestDataValidation.df['second_name'], 'second_name')
        self.check_optional_string(TestDataValidation.df['comments'], 'comments')
        self.check_comments_length(TestDataValidation.df['comments'], 'comments')
        self.check_date(TestDataValidation.df['date_of_birth'], 'date_of_birth')
        self.check_age(TestDataValidation.df['date_of_birth'], 'date_of_birth')
        self.check_unique(TestDataValidation.df['ssn'], 'ssn')
        self.check_in_list(TestDataValidation.df['bio_gender'], valid_genders, 'bio_gender')
        self.check_in_list(TestDataValidation.df['religion'], valid_religions, 'religion')
        self.check_in_list(TestDataValidation.df['race'], valid_races, 'race')
        self.check_optional_string(TestDataValidation.df['language'], 'language')
        self.check_single_uppercase_letter(TestDataValidation.df['voca_classifications'], 'voca_classifications')
        self.check_boolean(TestDataValidation.df['prior_convictions'], 'prior_convictions')
        self.check_boolean(TestDataValidation.df['convicted_against_children'], 'convicted_against_children')
        self.check_boolean(TestDataValidation.df['sexual_offender'], 'sexual_offender')
        self.check_boolean(TestDataValidation.df['sexual_predator'], 'sexual_predator')

if __name__ == '__main__':
    unittest.main()

