from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BonusCategory(models.Model):
    """
    Model for managing bonus categories.
    """
    _name = 'barbershop.bonus.category'
    _description = 'Bonus Category'

    name = fields.Char(
        string='Category Name',
        required=True,
        help='The name of the bonus category. Must be unique and at least 3 characters long.'
    )
    description = fields.Html(
        string='Description',
        help='Detailed description of the bonus category.'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Indicates whether the category is active.'
    )
    bonus_ids = fields.One2many(
        comodel_name='barbershop.bonus',
        inverse_name='category_id',
        string='Bonuses',
        help='List of bonuses associated with this category.'
    )

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'The category name must be unique!')
    ]

    @api.constrains('name')
    def _check_name(self):
        """
        Ensure that the category name is unique and at least 3 characters long.
        """
        for record in self:
            if len(record.name) < 3:
                raise ValidationError("The category name must be at least 3 characters long.")

    def activate_category(self):
        """
        Activate the category.
        """
        self.write({'active': True})

    def deactivate_category(self):
        """
        Deactivate the category.
        """
        self.write({'active': False})

    @api.model
    def create(self, vals):
        """
        Override create method to add custom logic.
        """
        if 'name' in vals and len(vals['name']) < 3:
            raise ValidationError("The category name must be at least 3 characters long.")
        return super(BonusCategory, self).create(vals)

    def write(self, vals):
        """
        Override write method to add custom logic.
        """
        if 'name' in vals and len(vals['name']) < 3:
            raise ValidationError("The category name must be at least 3 characters long.")
        return super(BonusCategory, self).write(vals)
