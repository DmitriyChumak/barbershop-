from odoo import models, fields, api
from odoo.exceptions import ValidationError

class WorkSchedule(models.Model):
    _name = 'barbershop.work.schedule'
    _description = 'Work Schedule'

    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
        help='The display name of the work schedule.'
    )
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Barber',
        required=True,
        domain="[('is_barber', '=', True)]",
        help='The barber associated with this work schedule.'
    )
    days_of_week = fields.Many2many(
        comodel_name='barbershop.days.of.week',
        string='Days of Week',
        required=True,
        help='Days of the week for the work schedule.'
    )
    start_time_work = fields.Float(
        string='Start Time',
        required=True,
        help="Start time of the work schedule in 24-hour format. Example: 9.5 for 9:30 AM."
    )
    end_time_work = fields.Float(
        string='End Time',
        required=True,
        help="End time of the work schedule in 24-hour format. Example: 18.0 for 6:00 PM."
    )
    break_ids = fields.One2many(
        comodel_name='barbershop.break',
        inverse_name='work_schedule_id',
        string='Breaks',
        ondelete='cascade',
        help='Break periods during the work schedule.'
    )
    holiday_ids = fields.One2many(
        comodel_name='barbershop.holiday',
        string='Holidays',
        compute='_compute_holiday_ids',
        help='Holidays associated with this work schedule.'
    )
    descriptions = fields.Html(
        string='Description'
    )

    @api.depends('employee_id', 'days_of_week')
    def _compute_display_name(self):
        """
        Compute the display name for the work schedule.
        """
        for record in self:
            days = ', '.join(record.days_of_week.mapped('name'))
            record.display_name = f"{record.employee_id.name} - {days}"

    @api.constrains('start_time_work', 'end_time_work')
    def _check_times(self):
        """
        Ensure that the start time is before the end time.
        """
        for record in self:
            if record.start_time_work >= record.end_time_work:
                raise ValidationError("The start time must be before the end time.")

    @api.constrains('break_ids')
    def _check_break_times(self):
        """
        Ensure that breaks are within the work schedule time range and their start time is before the end time.
        """
        for record in self:
            for break_period in record.break_ids:
                if break_period.start_time >= break_period.end_time:
                    raise ValidationError("The start time must be before the end time in break periods.")
                if not (record.start_time_work <= break_period.start_time < record.end_time_work and
                        record.start_time_work < break_period.end_time <= record.end_time_work):
                    raise ValidationError("Break periods must be within the work schedule time range.")

    @api.depends('employee_id')
    def _compute_holiday_ids(self):
        """
        Compute the list of all holidays associated with the selected barber.
        """
        for record in self:
            if record.employee_id:
                holidays = self.env['barbershop.holiday'].search([
                    ('employee_id', '=', record.employee_id.id),
                    ('start_date', '>=', fields.Date.today()),
                    ('end_date', '>=', fields.Date.today()),
                ])
                record.holiday_ids = holidays
            else:
                record.holiday_ids = False
