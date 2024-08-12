from odoo import models, fields


class DaysOfWeek(models.Model):
    """
    Model for days of the week.
    """
    _name = 'barbershop.days.of.week'
    _description = 'Days of the Week'

    name = fields.Char(
        string='Day',
        required=True,
        help='Name of the day of the week.'
    )
    sequence = fields.Integer(
            string='Order',
            required=True,
            help='The order of the day in the week, where Monday is 1 and Sunday is 7.'
    )