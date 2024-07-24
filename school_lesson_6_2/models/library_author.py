from odoo import models, fields, api
from datetime import timedelta


class LibraryAuthor(models.Model):
    """
    Model for Library Authors.

    This model defines the structure and behavior of authors in the library management system.
    """
    _name = 'library.author'
    _description = 'Library Author'

    first_name = fields.Char(string='First Name', translate=True)
    second_name = fields.Char(string='Second Name', translate=True)
    name = fields.Char(string='Author Name', compute='_compute_name', store=True)
    biography = fields.Text(string='Biography')
    create_date = fields.Datetime(string='Creation Date', default=fields.Datetime.now)
    recent_author = fields.Boolean(compute='_compute_recent_author', store=True)
    book_ids = fields.One2many(comodel_name='library.book', inverse_name='author_id', string='Books')

    @api.depends('create_date')
    def _compute_recent_author(self):
        """
        Compute method to determine if the author is recent.

        An author is considered recent if they were created in the last 30 days.
        """
        for record in self:
            recent_date = fields.Datetime.now() - timedelta(days=30)
            record.recent_author = record.create_date >= recent_date

    @api.depends('first_name', 'second_name')
    def _compute_name(self):
        """
        Compute method to generate the full name of the author.

        Combines the first name and second name into a single field.
        """
        for author in self:
            author.name = f"{author.first_name} {author.second_name}"
