from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Break(models.Model):
    """
    Model for managing break periods within work schedules for barbers.

    This model keeps track of break periods within a barber's work schedule, including
    the start and end times of each break.
    """
    _name = 'barbershop.break'
    _description = 'Break'

    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
        help='The display name of the break period.'
    )
    work_schedule_id = fields.Many2one(
        comodel_name='barbershop.work.schedule',
        string='Work Schedule',
        required=True,
        help='The work schedule associated with this break period.'
    )
    start_time = fields.Float(
        string='Start Time',
        required=True,
        help="Start time of the break in 24-hour format. Example: 12.0 for 12:00 PM."
    )
    end_time = fields.Float(
        string='End Time',
        required=True,
        help="End time of the break in 24-hour format. Example: 12.5 for 12:30 PM."
    )
    days_of_week = fields.Many2many(
        comodel_name='barbershop.days.of.week',
        string='Days of Week',
        required=True,
        help='Days of the week for the break period.'
    )
    description = fields.Html(
        string='Description'
    )

    @api.depends('start_time', 'end_time', 'days_of_week')
    def _compute_display_name(self):
        """
        Compute the display name for the break period.
        """
        for record in self:
            days = ', '.join(record.days_of_week.mapped('name'))
            record.display_name = f"Break: {record.start_time} - {record.end_time} on {days}"

    @api.constrains('start_time', 'end_time')
    def _check_times(self):
        """
        Ensure that the start time is before the end time.
        """
        for record in self:
            if record.start_time >= record.end_time:
                raise ValidationError("The start time must be before the end time.")
