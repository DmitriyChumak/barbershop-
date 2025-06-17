from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError


class Appointment(models.Model):
    _name = 'barbershop.appointment'
    _description = 'Barbershop Appointment'

    name = fields.Char(
        string='Name',
        compute='_compute_name',
        store=True,
        compute_sudo=True
    )
    customer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        required=True,
        help="The customer who booked the appointment."
    )
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Barber',
        required=True,
        domain="[('is_barber', '=', True)]",
        help="The barber assigned to perform the service."
    )
    service_id = fields.Many2one(
        comodel_name='barbershop.service',
        string='Service',
        required=True,
        help="The service booked for this appointment."
    )
    date_time = fields.Datetime(
        string='Date and Time',
        required=True,
        help="The scheduled date and time for the appointment."
    )
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='scheduled', help="The current status of the appointment.")

    notes = fields.Html(
        string='Notes',
        help="Additional notes or special requests for the appointment."
    )
    calendar_event_id = fields.Many2one(
        comodel_name='calendar.event',
        string='Calendar Event',
        help="The linked Odoo calendar event for this appointment."
    )
    service_cost = fields.Float(
        string='Service Cost',
        compute='_compute_service_cost',
        store=True,
        help='The cost of the service for this appointment.'
    )
    service_duration = fields.Float(
        string='Service Duration',
        compute='_compute_service_duration',
        store=True,
        help='The duration of the service for this appointment in hours.'
    )

    @api.constrains('date_time', 'employee_id', 'service_id', 'state')
    def _check_date_time(self):
        for record in self:
            if record.state == 'cancelled':
                return  # Skip validation for cancelled appointments

            if not record.date_time or not record.employee_id or not record.service_id:
                # This should ideally be caught by 'required=True' on fields
                # but good for robustness within the constraint.
                return

            # Ensure appointment date is in the future
            # Add a small grace period (e.g., 1 minute) to avoid issues with near-instantaneous creation/validation.
            if record.date_time < fields.Datetime.now() - timedelta(minutes=1):
                raise ValidationError("The appointment date and time must be in the future.")

            current_appt_start = record.date_time
            current_appt_duration_hours = record.service_duration

            if current_appt_duration_hours <= 0:
                raise ValidationError("The service duration must be a positive number of hours. Please check the service configuration.")

            current_appt_end = current_appt_start + timedelta(hours=current_appt_duration_hours)

            # Search for potentially overlapping appointments for the same barber
            # An appointment overlaps if its start time is before the current one ends,
            # AND its end time is after the current one starts.
            # Domain: ApptB_Start < CurrentAppt_End
            domain = [
                ('employee_id', '=', record.employee_id.id),
                ('id', '!=', record.id),
                ('state', '!=', 'cancelled'),
                ('date_time', '<', current_appt_end.strftime('%Y-%m-%d %H:%M:%S')),
            ]
            potential_overlaps = self.env['barbershop.appointment'].search(domain)

            for existing_appt in potential_overlaps:
                existing_appt_start = existing_appt.date_time
                existing_appt_duration_hours = existing_appt.service_duration

                if existing_appt_duration_hours <= 0:
                    # This indicates a data integrity issue with an existing appointment's service.
                    # Log it or skip. For now, skip to avoid blocking due to other bad data.
                    # Consider adding a logger.warning here in a real scenario.
                    continue

                existing_appt_end = existing_appt_start + timedelta(hours=existing_appt_duration_hours)

                # The core overlap condition: (StartA < EndB) and (EndA > StartB)
                if current_appt_start < existing_appt_end and current_appt_end > existing_appt_start:
                    raise ValidationError(
                        f"The barber {record.employee_id.name} has an overlapping appointment ('{existing_appt.name}') "
                        f"from {existing_appt_start.strftime('%H:%M')} to {existing_appt_end.strftime('%H:%M')} "
                        f"on {existing_appt_start.strftime('%Y-%m-%d')}."
                    )

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override the create method to create or update calendar events and reminders.

        :param vals_list: List of dictionaries of field values for the records to be created.
        :return: The created records.
        """
        records = super(Appointment, self).create(vals_list)
        records._create_or_update_calendar_event()
        return records

    def write(self, vals):
        """
        Override the write method to update calendar events and reminders.

        :param vals: Dictionary of field values to update the record.
        :return: True if the write operation was successful.
        """
        res = super(Appointment, self).write(vals)
        self._create_or_update_calendar_event()
        return res

    def unlink(self):
        """
        Override the unlink method to delete associated calendar events.

        :return: True if the unlink operation was successful.
        """
        self._delete_calendar_event()
        return super(Appointment, self).unlink()

    @api.depends('customer_id', 'date_time')
    def _compute_name(self):
        """
        Compute the name of the appointment based on the customer and date/time.
        """
        for appointment in self:
            if appointment.customer_id and appointment.date_time:
                appointment.name = f"{appointment.customer_id.name} - {appointment.date_time.strftime('%Y-%m-%d %H:%M')}"
            else:
                appointment.name = "New Appointment"

    def _create_or_update_calendar_event(self):
        """
        Create or update the calendar event and reminders for the appointment.
        """
        for appointment in self:
            start_time = appointment.date_time
            end_time = appointment.date_time + timedelta(hours=appointment.service_id.duration or 1)

            if not appointment.calendar_event_id:
                event = self.env['calendar.event'].create({
                    'name': f"Appointment with {appointment.customer_id.name}",
                    'start': start_time,
                    'stop': end_time,
                    'partner_ids': [(4, appointment.customer_id.id)],
                    'user_id': appointment.employee_id.user_id.id,
                })
                appointment.calendar_event_id = event.id
            else:
                event = appointment.calendar_event_id
                event.write({
                    'name': f"Appointment with {appointment.customer_id.name}",
                    'start': start_time,
                    'stop': end_time,
                })

            # Clear existing alarms
            event.write({'alarm_ids': [(5, 0, 0)]})

            # Reminder lead times are configurable via System Parameters:
            # 'barbershop.reminder_barber_minutes' (default: 15)
            # 'barbershop.reminder_customer_minutes' (default: 120)
            config_param = self.env['ir.config_parameter'].sudo()
            try:
                barber_reminder_minutes = int(config_param.get_param('barbershop.reminder_barber_minutes', default='15'))
            except ValueError:
                barber_reminder_minutes = 15 # Fallback if non-integer in db
            try:
                customer_reminder_minutes = int(config_param.get_param('barbershop.reminder_customer_minutes', default='120'))
            except ValueError:
                customer_reminder_minutes = 120 # Fallback

            if barber_reminder_minutes <= 0: # Ensure positive
                barber_reminder_minutes = 15
            if customer_reminder_minutes <= 0: # Ensure positive
                customer_reminder_minutes = 120

            # Barber Reminder
            barber_alarm_vals = {
                'name': 'Barber Reminder via Notification',
                'alarm_type': 'notification',
                'duration': barber_reminder_minutes,
                'interval_unit': 'minutes',
            }

            # Customer Reminder
            customer_alarm_vals = {
                'name': 'Customer Reminder via Email',
                'alarm_type': 'email',
                'duration': customer_reminder_minutes,
                'interval_unit': 'minutes',
            }

            event.write({
                'alarm_ids': [
                    (0, 0, barber_alarm_vals),
                    (0, 0, customer_alarm_vals)
                ]
            })

    def _delete_calendar_event(self):
        """
        Delete the associated calendar event for the appointment.
        """
        for appointment in self:
            if appointment.calendar_event_id:
                appointment.calendar_event_id.unlink()

    def change_state(self, new_state):
        """
        Change the state of the appointment.

        :param new_state: The new state to set.
        """
        for record in self:
            record.state = new_state

    def action_set_state_scheduled(self):
        """
        Action to set the state to 'scheduled'.
        """
        self.change_state('scheduled')

    def action_set_state_completed(self):
        """
        Action to set the state to 'completed'.
        """
        self.change_state('completed')

    def action_set_state_cancelled(self):
        """
        Action to set the state to 'cancelled'.
        """
        self.change_state('cancelled')

    @api.depends('service_id.price')
    def _compute_service_cost(self):
        for record in self:
            if record.service_id:
                record.service_cost = record.service_id.price
            else:
                record.service_cost = 0.0

    @api.depends('service_id.duration')
    def _compute_service_duration(self):
        for record in self:
            if record.service_id:
                record.service_duration = record.service_id.duration
            else:
                record.service_duration = 0.0
