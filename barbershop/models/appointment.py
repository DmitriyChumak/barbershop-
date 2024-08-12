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
        required=True
    )
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Barber',
        required=True,
        domain="[('is_barber', '=', True)]"
    )
    service_id = fields.Many2one(
        comodel_name='barbershop.service',
        string='Service',
        required=True
    )
    date_time = fields.Datetime(
        string='Date and Time',
        required=True
    )
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='scheduled')

    notes = fields.Html(
        string='Notes'
    )
    calendar_event_id = fields.Many2one(
        comodel_name='calendar.event',
        string='Calendar Event'
    )

    REMINDER_BARBER_MINUTES = 15
    REMINDER_CUSTOMER_HOURS = 2

    @api.constrains('date_time')
    def _check_date_time(self):
        """
        Ensure that the appointment date and time are in the future and that
        the barber has no overlapping appointments.
        """
        for record in self:
            if record.date_time < fields.Datetime.now():
                raise ValidationError("The appointment date and time must be in the future.")

            overlapping_appointments = self.env['barbershop.appointment'].search([
                ('employee_id', '=', record.employee_id.id),
                ('date_time', '<', record.date_time + timedelta(hours=record.service_id.duration or 1)),
                ('date_time', '>', record.date_time - timedelta(minutes=15)),
                ('id', '!=', record.id),
            ])
            if overlapping_appointments:
                raise ValidationError("The barber has another appointment at this time.")

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
                appointment.calendar_event_id.write({
                    'name': f"Appointment with {appointment.customer_id.name}",
                    'start': start_time,
                    'stop': end_time,
                })

            self._create_reminders(appointment)

    def _delete_calendar_event(self):
        """
        Delete the associated calendar event for the appointment.
        """
        for appointment in self:
            if appointment.calendar_event_id:
                appointment.calendar_event_id.unlink()

    def _create_reminders(self, appointment):
        """
        Create reminders for the barber and customer for the appointment.

        :param appointment: The appointment record.
        """
        Reminder = self.env['calendar.event']

        # Create reminder for the barber
        reminder_barber_date = appointment.date_time - timedelta(minutes=self.REMINDER_BARBER_MINUTES)
        Reminder.create({
            'name': f'Reminder: {appointment.service_id.name} for Barber',
            'customer_id': appointment.employee_id.user_id.partner_id.id,
            'appointment_id': appointment.id,
            'location': 'Barbershop',
            'start': reminder_barber_date,
            'stop': reminder_barber_date + timedelta(hours=1),
            'reminder_date': reminder_barber_date,
        })

        # Create reminder for the customer
        reminder_customer_date = appointment.date_time - timedelta(hours=self.REMINDER_CUSTOMER_HOURS)
        Reminder.create({
            'name': f'Reminder: {appointment.service_id.name} for Customer',
            'customer_id': appointment.customer_id.id,
            'appointment_id': appointment.id,
            'location': 'Barbershop',
            'start': reminder_customer_date,
            'stop': reminder_customer_date + timedelta(hours=1),
            'reminder_date': reminder_customer_date,
        })

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
