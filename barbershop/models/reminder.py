from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError


class Reminder(models.Model):
    _inherit = ['calendar.event']

    customer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        required=True,
        help="The customer for whom the reminder is set."
    )
    appointment_id = fields.Many2one(
        comodel_name='barbershop.appointment',
        string='Appointment',
        required=True,
        help="The appointment associated with the reminder."
    )
    reminder_date = fields.Datetime(
        string='Reminder Date',
        required=True,
        help="The date and time when the reminder is set."
    )

    @api.model
    def create_reminder(self, appointment_id, reminder_date):
        """
        Create a reminder for the given appointment.

        :param appointment_id: The ID of the appointment for which to create the reminder.
        :param reminder_date: The date and time when the reminder should be set.
        """
        appointment = self.env['barbershop.appointment'].browse(appointment_id)
        if not appointment:
            raise ValidationError("Appointment not found.")
        self.create({
            'name': f'Reminder: {appointment.service_id.name}',
            'customer_id': appointment.customer_id.id,
            'appointment_id': appointment_id,
            'start': reminder_date,
            'stop': reminder_date + timedelta(hours=1),  # Duration of 1 hour for the reminder
            'reminder_date': reminder_date,
        })
