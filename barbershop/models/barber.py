from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class Barber(models.Model):
    """
      Extension of the hr.employee model to represent Barbers in the Barbershop module.

      This model adds additional fields and constraints specific to Barbers,
      including work schedules, holidays, specializations, and appointment management.
      """
    _inherit = ['hr.employee']

    is_barber = fields.Boolean(
        string='Is a Barber',
        default=True
    )
    is_administrator = fields.Boolean(
        string='Is Administrator',
        default=False
    )
    work_schedule_ids = fields.One2many(
        comodel_name='barbershop.work.schedule',
        inverse_name='employee_id',
        string='Work Schedules'
    )
    holiday_ids = fields.One2many(
        comodel_name='barbershop.holiday',
        inverse_name='employee_id',
        string='Holidays'
    )
    specialization_ids = fields.Many2many(
        comodel_name='barbershop.specialization',
        string='Specializations'
    )
    service_ids = fields.Many2many(
        comodel_name='barbershop.service',
        string='Services'
    )
    appointment_ids = fields.One2many(
        comodel_name='barbershop.appointment',
        inverse_name='employee_id',
        string='Appointments'
    )
    bonus_ids = fields.One2many(
        comodel_name='barbershop.bonus',
        inverse_name='employee_id',
        string='Bonuses'
    )
    bonus_percentage = fields.Float(
        string='Bonus Percentage',
        default=10.0
    )

    @api.constrains('is_barber', 'specialization_ids')
    def _check_specializations(self):
        """
        Ensure that every barber has at least one specialization.
        """
        for record in self:
            if record.is_barber and not record.specialization_ids:
                raise ValidationError("A barber must have at least one specialization.")

    @api.constrains('bonus_percentage')
    def _check_bonus_percentage(self):
        """
        Ensure that the bonus percentage is between 0 and 100.
        """
        for record in self:
            if record.bonus_percentage <= 0 or record.bonus_percentage > 100:
                raise ValidationError("The bonus percentage must be between 0 and 100.")

    def get_available_slots(self, date):
        """
        Get available time slots for this barber on a given date.

        :param date: datetime.date object representing the date for which to get available slots.
        :return: list of available time slots as strings in 'HH:MM' format.
        """
        self.ensure_one()
        appointments = self.env['barbershop.appointment'].search([
            ('employee_id', '=', self.id),
            ('date_time', '>=', date),
            ('date_time', '<', date + timedelta(days=1)),
            ('state', '=', 'scheduled')
        ])

        work_schedules = self.env['barbershop.work.schedule'].search([
            ('employee_id', '=', self.id),
            ('day_of_week', '=', date.weekday())
        ])

        holidays = self.env['barbershop.holiday'].search([
            ('employee_id', '=', self.id),
            ('date', '=', date)
        ])

        if holidays:
            return []  # No available slots on holidays

        slots = []
        for schedule in work_schedules:
            current_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=schedule.start_time)
            end_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=schedule.end_time)
            for break_period in schedule.break_ids:
                break_start = datetime.combine(date, datetime.min.time()) + timedelta(hours=break_period.start_time)
                break_end = datetime.combine(date, datetime.min.time()) + timedelta(hours=break_period.end_time)
                while current_time < end_time:
                    slot_end_time = current_time + timedelta(minutes=15)
                    if (current_time < break_start or slot_end_time > break_end) and not appointments.filtered(
                            lambda a: a.date_time < slot_end_time and a.date_time + timedelta(
                                hours=a.service_id.duration or 1) > current_time):
                        slots.append(current_time.strftime('%H:%M'))
                    current_time = slot_end_time

        return slots

    @api.constrains('work_schedule_ids')
    def _check_work_schedules(self):
        """
        Ensure that the work schedules are valid.
        """
        for record in self:
            for schedule in record.work_schedule_ids:
                if schedule.start_time >= schedule.end_time:
                    raise ValidationError("The start time must be before the end time in work schedules.")
                for break_period in schedule.break_ids:
                    if break_period.start_time >= break_period.end_time:
                        raise ValidationError("The start time must be before the end time in break periods.")
                    if not (schedule.start_time <= break_period.start_time < schedule.end_time and
                            schedule.start_time < break_period.end_time <= schedule.end_time):
                        raise ValidationError("Break periods must be within the work schedule time range.")
