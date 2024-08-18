from odoo import models, fields, api


class BarberLoadReportWizard(models.TransientModel):
    _name = 'barbershop.barber_load_report_wizard'
    _description = 'Barber Load Report Wizard'

    date_start = fields.Date(string="Start Date", required=True)
    date_end = fields.Date(string="End Date", required=True)

    def generate_report(self):
        data = {
            'date_start': self.date_start,
            'date_end': self.date_end,
        }
        return self.env.ref('barbershop.action_report_barber_load').report_action(self, data=data)
