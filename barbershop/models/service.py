from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Service(models.Model):
    """
    Model for managing services offered by the barbershop.
    """
    _name = 'barbershop.service'
    _description = 'Barbershop Service'

    name = fields.Char(
        string='Service Name',
        required=True,
        help='The name of the service offered by the barbershop.'
    )
    duration = fields.Float(
        string='Duration (hours)',
        required=True,
        help='The duration of the service in hours.'
    )
    price = fields.Float(
        string='Price',
        required=True,
        help='The price of the service.'
    )
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('unisex', 'Unisex'),
    ], string='Gender',
        default='unisex',
        required=True,
        help='The gender for which the service is suitable.'
    )
    description = fields.Html(
        string='Description',
        help='A detailed description of the service.'
    )
    specialization_ids = fields.Many2many(
        comodel_name='barbershop.specialization',
        string='Specializations',
        help='The specializations associated with this service.'
    )
    employee_ids = fields.Many2many(
        comodel_name='hr.employee',
        string='Barbers',
        domain="[('is_barber', '=', True)]",
        help='The barbers who can perform this service.'
    )
    image = fields.Binary(
        string='Image',
        attachment=True,
        help='This field holds the image used as avatar for this service, limited to 1024x1024px.'
    )

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'The service name must be unique!'),
        ('positive_duration', 'CHECK(duration > 0)', 'The duration must be greater than zero.'),
        ('positive_price', 'CHECK(price > 0)', 'The price must be greater than zero.')
    ]

    @api.constrains('specialization_ids')
    def _check_specializations(self):
        """
        Ensure that the service has at least one specialization.
        """
        for record in self:
            if not record.specialization_ids:
                raise ValidationError("The service must be associated with at least one specialization.")

    @api.constrains('employee_ids')
    def _check_barbers(self):
        """
        Ensure that the service has at least one barber.
        """
        for record in self:
            if not record.employee_ids:
                raise ValidationError("The service must be associated with at least one barber.")
