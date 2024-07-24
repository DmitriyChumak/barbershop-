from odoo import models, fields, api

class LibraryBook(models.Model):
    """
    Model for Library Books, inherited from the base 'library.book' model.

    This model adds an author relationship and custom behaviors for the library books.
    """
    _inherit = 'library.book'

    author_id = fields.Many2one(
        comodel_name='library.author',
        string='Author'
    )

    @api.model
    def default_get(self, fields_list):
        """
        Override the default_get method to set default values.

        By default, sets the 'is_active' field to True.
        """
        res = super(LibraryBook, self).default_get(fields_list)
        res.update({
            'is_active': True,
        })
        return res

    def action_scrap_book(self):
        """
        Custom method to mark books as inactive.

        This method sets the 'is_active' field to False for each book in the recordset.
        """
        for book in self:
            book.is_active = False
