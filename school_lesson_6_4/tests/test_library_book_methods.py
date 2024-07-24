from odoo.tests.common import TransactionCase, tagged


@tagged('odooschool')
class TestLibraryBookMethods(TransactionCase):
    """
    Test cases for methods in the library.book model.

    This class contains tests to verify the behavior of custom methods in the library.book model.
    """

    def setUp(self):
        """
        Set up the test environment.

        This method initializes the test environment, creates a test author, and a test book.
        """
        super(TestLibraryBookMethods, self).setUp()
        # Create a test author
        self.author_mark_twain = self.env['library.author'].create({
            'first_name': 'Mark',
            'second_name': 'Twain'
        })
        # Create a test book
        self.book = self.env['library.book'].create({
            'name': 'The Adventures of Tom Sawyer',
            'author_id': self.author_mark_twain.id
        })

    def test_action_scrap_book(self):
        """
        Test the action_scrap_book method.

        This test verifies that the book is initially active and becomes inactive after calling the action_scrap_book method.
        """
        # Check initial state of the book
        self.assertTrue(self.book.is_active, "Book should be active initially.")

        # Call the action_scrap_book method
        self.book.action_scrap_book()

        # Check the state of the book after calling the method
        self.assertFalse(self.book.is_active, "Book should be inactive after scrapping.")
