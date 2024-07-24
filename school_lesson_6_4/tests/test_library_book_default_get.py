from odoo.tests.common import TransactionCase, Form, tagged


@tagged('odooschool')
class TestLibraryBookDefaultGet(TransactionCase):
    """
    Test cases for the default values in the library.book model.

    This class contains tests to verify the default values when creating a new book record.
    """

    def setUp(self):
        """
        Set up the test environment.

        This method initializes the test environment and creates a test author record.
        """
        super(TestLibraryBookDefaultGet, self).setUp()
        # Create a test author
        self.author_mark_twain = self.env['library.author'].create({
            'first_name': 'Mark',
            'second_name': 'Twain'
        })

    def test_default_get(self):
        """
        Test the default values for a new book record.

        This test creates a new book using a form and checks the default values for the 'is_active', 'name', and 'author_id' fields.
        """
        # Create a form for the library.book model
        with Form(self.env['library.book']) as f:
            f.name = 'New Book'
            f.author_id = self.author_mark_twain

        new_book = f.save()

        # Check default values
        self.assertEqual(new_book.is_active, True, "Default value for 'is_active' should be True")
        self.assertEqual(new_book.name, 'New Book', "Book name should be 'New Book'")
        self.assertEqual(new_book.author_id, self.author_mark_twain, "Author should be 'Mark Twain'")
