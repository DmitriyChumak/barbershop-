from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Holiday(models.Model):
    """
    Model for managing holidays for barbers in the barbershop module.
    This model keeps track of the holidays for each barber, including the date
    and a description of the holiday.
    """
    _name = 'barbershop.holiday'
    _description = 'Holiday'

    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
        help='The display name of the holiday.'
    )
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Barber',
        required=True,
        domain="[('is_barber', '=', True)]",
        help='The barber associated with this holiday.'
    )
    work_schedule_id = fields.Many2one(
        comodel_name='barbershop.work.schedule',
        string='Work Schedule',
        ondelete='cascade',
        help='The work schedule associated with this holiday.'
    )
    start_date = fields.Date(
        string='Start Date',
        required=True,
        help='The start date of the holiday.'
    )
    end_date = fields.Date(
        string='End Date',
        required=True,
        help='The end date of the holiday.'
    )
    description = fields.Html(
        string='Description',
        help='A brief description of the holiday.'
    )

    _sql_constraints = [
        ('unique_holiday_barber_date', 'unique(employee_id, start_date, end_date)', 'A barber cannot have overlapping holidays.')
    ]

    @api.depends('employee_id', 'start_date', 'end_date')
    def _compute_display_name(self):
        """
        Compute the display name for the holiday.
        """
        for record in self:
            record.display_name = f"{record.employee_id.name} - {record.start_date} to {record.end_date}"

    @api.constrains('start_date', 'end_date')
    def _check_holiday_date(self):
        """
        Ensure that the holiday date is not in the past and start date is before end date.
        """
        for record in self:
            if record.start_date < fields.Date.today() or record.end_date < fields.Date.today():
                raise ValidationError("The holiday date cannot be in the past.")
            if record.start_date > record.end_date:
                raise ValidationError("The start date must be before the end date.")

