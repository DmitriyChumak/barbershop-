from odoo import api, fields, models, exceptions


class LibraryBook(models.Model):
    """
    This model represents a library book with its attributes and business logic.
    """
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(
        string='Title',
        required=True,
        help='The title of the book'
    )
    category_id = fields.Many2one(
        comodel_name='library.book.category',
        string='Category',
        help='Category of the book'
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User',
        default=lambda self: self.env.ref('base.user_admin').id,
        help='User responsible for the book'
    )
    reader_id = fields.Many2one(
        comodel_name='res.partner',
        string='Reader',
        help='Partner who is reading the book'
    )
    checkout_date = fields.Date(
        string='Checkout Date',
        readonly=True,
        help='Date when the book was checked out'
    )
    return_date = fields.Date(
        string='Return Date',
        help='Date when the book was returned'
    )
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Indicates if the book is active'
    )

    @api.model
    def create(self, vals):
        """
        Overrides the create method to set the checkout date if a reader is assigned.

        :param vals: dictionary of values for creating a new record
        :return: newly created record
        """
        if vals.get('reader_id'):
            vals['checkout_date'] = fields.Date.today()
        return super(LibraryBook, self).create(vals)

    def write(self, vals):
        """
        Overrides the write method to update checkout and return dates based on reader assignment.

        :param vals: dictionary of values to write to the record
        :return: boolean indicating success
        """
        if vals.get('reader_id'):
            vals['checkout_date'] = fields.Date.today()
        elif 'reader_id' in vals and not vals['reader_id']:
            vals['return_date'] = fields.Date.today()
        return super(LibraryBook, self).write(vals)

    @api.constrains('reader_id')
    def _check_reader(self):
        """
        Ensures that a book cannot be checked out by another reader if it is already checked out.

        :raises ValidationError: if the book is already checked out
        """
        if self.reader_id and self.checkout_date and not self.return_date:
            raise exceptions.ValidationError('The book is already checked out by another reader.')

    def action_return_book(self):
        """
        Marks the book as returned by clearing the reader and dates.

        :return: void
        """
        self.ensure_one()
        self.return_date = fields.Date.today()
        self.reader_id = False
        self.checkout_date = False

    def action_assign_default_reader(self):
        """
        Assigns the default reader (admin) to the book.

        :return: void
        """
        self.ensure_one()
        self.reader_id = self.env.ref('base.partner_admin').id
