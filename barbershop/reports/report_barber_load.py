from odoo import models, fields, api


class ReportBarberLoad(models.Model):
    _name = 'report.barber.load'
    _description = 'Report Barber Load'
    _auto = False

    employee_id = fields.Many2one('hr.employee', string='Barber')
    appointment_count = fields.Integer(string='Number of Appointments')

    # @api.model
    # def _select(self):
    #     return """
    #         SELECT
    #             row_number() OVER () AS id,
    #             employee_id,
    #             count(id) as appointment_count
    #         FROM
    #             barbershop_appointment
    #         WHERE
    #             id IS NOT NULL
    #         GROUP BY
    #             employee_id
    #     """
    #
    # @api.model
    # def init(self):
    #     self.env.cr.execute("""
    #         CREATE OR REPLACE VIEW report_barber_load AS (%s)
    #     """ % (self._select()))
