from odoo import models, fields


class LibraryBookCategory(models.Model):
    """
    Model for representing a library book category.

    Attributes:
        name (Char): The name of the category.
        description (Text): The description of the category.
        book_ids (One2many): Reference to the books in this category.
    """
    _name = 'library.book.category'
    _description = 'Library Book Category'

    name = fields.Char(
        string='Category',
        required=True,
        help='Category name'
    )
    description = fields.Text(
        string='Description',
        help='Description of the category'
    )
    book_ids = fields.One2many(
        comodel_name='library.book',
        inverse_name='category_id',
        string='Books',
        help='Books in this category'
    )

    def action_books_this_category(self):
        """
        Returns an action to view books in this category.

        This method returns a dictionary with the action parameters to view books filtered by this category.

        :return: dict
        """
        return {
            'name': 'Books',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'library.book',
            'domain': [('category_id', '=', self.id)],
        }
