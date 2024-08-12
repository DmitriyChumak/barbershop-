from odoo import models, fields, api


class Customer(models.Model):
    _inherit = ['res.partner']

    is_barbershop_customer = fields.Boolean(
        string='Barbershop Customer',
        default=True
    )
    appointment_ids = fields.One2many(
        comodel_name='barbershop.appointment',
        inverse_name='customer_id',
        string='Appointments'
    )
    last_visit_date = fields.Date(
        string='Last Visit Date',
        compute='_compute_last_visit_date',
        store=True
    )
    total_spent = fields.Float(
        string='Total Spent',
        compute='_compute_total_spent',
        store=True
    )

    @api.depends('appointment_ids.state', 'appointment_ids.date_time')
    def _compute_last_visit_date(self):
        """
        Compute the date of the last completed appointment for the customer.
        """
        for partner in self:
            last_appointment = self.env['barbershop.appointment'].search(
                [('customer_id', '=', partner.id), ('state', '=', 'completed')],
                order='date_time desc',
                limit=1
            )
            partner.last_visit_date = last_appointment.date_time if last_appointment else None

    @api.depends('appointment_ids.state', 'appointment_ids.service_id.price')
    def _compute_total_spent(self):
        """
        Compute the total amount spent by the customer on completed appointments.
        """
        for partner in self:
            appointments = self.env['barbershop.appointment'].search(
                [('customer_id', '=', partner.id), ('state', '=', 'completed')]
            )
            total = sum(appointment.service_id.price for appointment in appointments)
            partner.total_spent = total
