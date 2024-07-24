from odoo import models, fields, api


class LibraryBookCategory(models.Model):
    """
    Inherited model for Library Book Category.

    This model inherits the 'library.book.category' model to add custom methods and behaviors.
    """
    _inherit = 'library.book.category'

    @api.depends()
    def get_books(self):
        """
        Returns a list of all books that belong to the current category.

        This method ensures that it is called on a single record and searches for all books
        associated with the current category.
        """
        self.ensure_one()  # Ensures that the method is called on a single record
        return self.env['library.book'].search([('category_id', '=', self.id)])
