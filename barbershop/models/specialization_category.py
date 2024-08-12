from odoo import models, fields


class SpecializationCategory(models.Model):
    """
       Model for managing barber specializations categories.
       """
    _name = 'barbershop.specialization.category'
    _description = 'Specialization Category'

    name = fields.Char(
        string='Name',
        required=True,
        help='The name of the specialization category.'
    )
    description = fields.Html(
        string='Description',
        help='A detailed description of the specialization category.'
    )
    specialization_ids = fields.One2many(
        comodel_name='barbershop.specialization',
        inverse_name='category_id',
        string='Specializations',
        help='The list of specializations under this category.'
    )
