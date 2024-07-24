from odoo.tests.common import TransactionCase

class TestAuthorUsage(TransactionCase):
    """
    Test cases for the usage of the author model.

    This class contains tests to verify the correct usage and properties of the author Mark Twain.
    """

    def setUp(self):
        """
        Set up the test environment.

        This method initializes the test environment and loads the common test record for author Mark Twain.
        """
        super(TestAuthorUsage, self).setUp()
        # Use the common test record for author Mark Twain
        self.author_mark_twain = self.env.ref('school_lesson_6_4.author_mark_twain')

    def test_usage_of_author(self):
        """
        Test the usage of the author Mark Twain.

        This test checks if the author Mark Twain has the correct first and second names.
        """
        # Assert that the first name of the author is 'Mark'
        self.assertEqual(self.author_mark_twain.first_name, 'Mark')
        # Assert that the second name of the author is 'Twain'
        self.assertEqual(self.author_mark_twain.second_name, 'Twain')
