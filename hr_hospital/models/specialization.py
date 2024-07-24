# specialization model

from odoo import models, fields


class Specialization(models.Model):
    _name = 'hr_hospital.specialization'
    _description = 'Specialization'

    name = fields.Char(
        string='Name',
        required=True
    )

    description = fields.Text(string='Description')
