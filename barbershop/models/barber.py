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
        default=True,
        help="Check this box if the employee is a barber and can be scheduled for appointments."
    )
    is_administrator = fields.Boolean(
        string='Is Administrator',
        default=False,
        help="Check this box if the employee has administrative privileges for the barbershop module."
    )
    work_schedule_ids = fields.One2many(
        comodel_name='barbershop.work.schedule',
        inverse_name='employee_id',
        string='Work Schedules',
        help="Define the regular working hours and breaks for this barber."
    )
    holiday_ids = fields.One2many(
        comodel_name='barbershop.holiday',
        inverse_name='employee_id',
        string='Holidays',
        help="Define any holidays or time off for this barber."
    )
    specialization_ids = fields.Many2many(
        comodel_name='barbershop.specialization',
        string='Specializations',
        help="The services this barber is specialized in."
    )
    service_ids = fields.Many2many(
        comodel_name='barbershop.service',
        string='Services',
        help="The specific services this barber can perform (often derived from specializations)."
    )
    appointment_ids = fields.One2many(
        comodel_name='barbershop.appointment',
        inverse_name='employee_id',
        string='Appointments',
        help="Appointments scheduled for this barber."
    )
    bonus_ids = fields.One2many(
        comodel_name='barbershop.bonus',
        inverse_name='employee_id',
        string='Bonuses',
        help="Bonuses accrued by this barber."
    )
    bonus_percentage = fields.Float(
        string='Bonus Percentage',
        default=10.0,
        help="The percentage of service price used for bonus calculation (e.g., 10 for 10%). Must be between 0 and 100."
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

        Get available time slots for this barber on a given date, considering work schedules,
        breaks, existing appointments, and holidays. The interval for slots is configurable
        via system parameter 'barbershop.slot_interval_minutes'.

        :param date: datetime.date object representing the date for which to get available slots.
        :return: list of available time slots as strings in 'HH:MM' format, sorted and unique.
        """
        self.ensure_one()

        # The time slot interval for availability display is configurable via System Parameter:
        # 'barbershop.slot_interval_minutes' (default: 15)
        # Fetch slot interval from system parameters
        config_param = self.env['ir.config_parameter'].sudo()
        try:
            slot_interval_minutes = int(config_param.get_param('barbershop.slot_interval_minutes', default='15'))
        except ValueError:
            slot_interval_minutes = 15
        if slot_interval_minutes <= 0:  # Ensure positive
            slot_interval_minutes = 15

        # Check for holidays
        holidays = self.env['barbershop.holiday'].search([
            ('employee_id', '=', self.id),
            ('start_date', '<=', date),
            ('end_date', '>=', date)
        ])
        if holidays:
            return []  # No available slots on holidays

        # Get work schedules for the given day
        day_record = self.env['barbershop.days.of.week'].search([
            ('sequence', '=', date.isoweekday())
        ], limit=1)
        if not day_record: # Should not happen if days_of_week data is correct
            return []

        work_schedules = self.env['barbershop.work.schedule'].search([
            ('employee_id', '=', self.id),
            ('days_of_week', 'in', day_record.ids)
        ])
        if not work_schedules:
            return [] # No work schedule for this day

        # Prepare busy appointment intervals
        appointments_for_day = self.env['barbershop.appointment'].search([
            ('employee_id', '=', self.id),
            ('state', '!=', 'cancelled'),
            ('date_time', '>=', datetime.combine(date, datetime.min.time())),
            ('date_time', '<', datetime.combine(date + timedelta(days=1), datetime.min.time())),
        ])
        busy_appointment_intervals = []
        for appt in appointments_for_day:
            if appt.service_duration > 0:  # service_duration is in hours
                appt_start = appt.date_time
                appt_end = appt_start + timedelta(hours=appt.service_duration)
                busy_appointment_intervals.append((appt_start, appt_end))

        # Prepare all break intervals for the day from active work schedules
        all_break_intervals = []
        for schedule in work_schedules: # Iterate through the fetched work_schedules for the day
            for break_period in schedule.break_ids:
                break_start_dt = datetime.combine(date, datetime.min.time()) + timedelta(hours=break_period.start_time)
                break_end_dt = datetime.combine(date, datetime.min.time()) + timedelta(hours=break_period.end_time)
                all_break_intervals.append((break_start_dt, break_end_dt))

        slots = []
        for schedule in work_schedules:
            schedule_start_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=schedule.start_time_work)
            schedule_end_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=schedule.end_time_work)
            current_time = schedule_start_time

            while current_time < schedule_end_time:
                slot_start_dt = current_time
                slot_end_dt = current_time + timedelta(minutes=slot_interval_minutes)

                if slot_end_dt > schedule_end_time:  # Do not exceed schedule
                    break

                is_slot_available = True

                # Check against breaks
                for break_start, break_end in all_break_intervals:
                    if max(slot_start_dt, break_start) < min(slot_end_dt, break_end):  # Overlap
                        is_slot_available = False
                        break
                if not is_slot_available:
                    current_time += timedelta(minutes=slot_interval_minutes)
                    continue

                # Check against appointments
                for appt_start, appt_end in busy_appointment_intervals:
                    if max(slot_start_dt, appt_start) < min(slot_end_dt, appt_end):  # Overlap
                        is_slot_available = False
                        break
                if not is_slot_available:
                    current_time += timedelta(minutes=slot_interval_minutes)
                    continue

                if is_slot_available:
                    slots.append(slot_start_dt.strftime('%H:%M'))

                current_time += timedelta(minutes=slot_interval_minutes)

        return sorted(list(set(slots))) # Ensure uniqueness and order

    @api.constrains('work_schedule_ids')
    def _check_work_schedules(self):
        """
        Ensure that the work schedules are valid.
        """
        for record in self:
            for schedule in record.work_schedule_ids:
                if schedule.start_time_work >= schedule.end_time_work:
                    raise ValidationError("The start time must be before the end time in work schedules.")
                for break_period in schedule.break_ids:
                    if break_period.start_time >= break_period.end_time:
                        raise ValidationError("The start time must be before the end time in break periods.")
                    if not (schedule.start_time_work <= break_period.start_time < schedule.end_time_work and
                            schedule.start_time_work < break_period.end_time <= schedule.end_time_work):
                        raise ValidationError("Break periods must be within the work schedule time range.")
