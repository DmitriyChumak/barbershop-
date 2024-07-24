from odoo.tests.common import TransactionCase


class TestLibraryUserPermissions(TransactionCase):
    """
    Test cases for library user permissions.

    This class contains tests to verify that users with "Library User" rights have the correct permissions.
    """

    def setUp(self):
        """
        Set up the test environment.

        This method initializes the test environment, creates a test author, a "Library User" group,
        and a user with "Library User" rights. It also references the admin user.
        """
        super(TestLibraryUserPermissions, self).setUp()
        # Create a record for author Mark Twain to use in tests
        self.author_mark_twain = self.env.ref('school_lesson_6_4.author_mark_twain')
        # Create a "Library User" group
        self.library_user_group = self.env.ref('school_lesson_6_2.group_library_user')
        # Create a user with "Library User" rights
        self.library_user = self.env['res.users'].create({
            'name': 'Library User',
            'login': 'library_user',
            'password': 'library_user',
            'groups_id': [(6, 0, [self.library_user_group.id])],
        })
        # Create an author record with admin user
        self.admin_user = self.env.ref('base.user_admin')

    def test_library_user_cannot_create_author(self):
        """
        Test that a library user cannot create a new author.

        This test switches the environment to the library user and tries to create a new author,
        expecting an exception to be raised.
        """
        # Switch to "Library User" and try to create a new author
        self.env = self.env(user=self.library_user)
        with self.assertRaises(Exception):
            self.env['library.author'].create({
                'first_name': 'New',
                'second_name': 'Author',
            })

    def test_library_user_cannot_access_author_form(self):
        """
        Test that a library user cannot access the author form view.

        This test switches the environment to the library user and tries to access the author form view,
        expecting an exception to be raised.
        """
        # Switch to "Library User" and check access to author form view
        self.env = self.env(user=self.library_user)
        with self.assertRaises(Exception):
            self.env['library.author'].search([])
