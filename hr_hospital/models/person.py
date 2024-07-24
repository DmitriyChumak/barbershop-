# person model

from odoo import models, fields, api
from datetime import date
# from odoo.exceptions import ValidationError


class Person(models.AbstractModel):
    _name = 'hr_hospital.person'
    _description = 'Person'

    first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name')
    birthdate = fields.Date(string='Birthdate')
    phone = fields.Char(string='Phone')
    photo = fields.Binary(string='Photo')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    address = fields.Text(string='Address')
    email = fields.Char(string='Email')

    name = fields.Char(
        string='Name',
        compute='_compute_names',
        store=True
    )

    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=True
    )

    @api.depends('first_name', 'last_name')
    def _compute_names(self):
        for record in self:
            if record.first_name and record.last_name:
                record.name = f'{record.first_name} {record.last_name}'.strip()
            else:
                record.name = "Unnamed Person"

    @api.depends('birthdate')
    def _compute_age(self):
        for record in self:
            if record.birthdate:
                today = date.today()
                try:
                    birth_date = fields.Date.from_string(record.birthdate)
                    record.age = today.year - birth_date.year - (
                            (today.month, today.day) < (birth_date.month, birth_date.day)
                    )
                except (ValueError, TypeError) as e:
                    record.age = 0
            else:
                record.age = 0

    # @api.model
    # def create(self, vals):
    #     if 'birthdate' in vals:
    #         try:
    #             vals['birthdate'] = datetime.strptime(vals['birthdate'], '%d-%m-%Y').strftime('%Y-%m-%d')
    #         except ValueError:
    #             raise ValidationError("Incorrect date format, should be DD-MM-YYYY")
    #     return super(Person, self).create(vals)
    #
    # def write(self, vals):
    #     if 'birthdate' in vals:
    #         try:
    #             vals['birthdate'] = datetime.strptime(vals['birthdate'], '%d-%m-%Y').strftime('%Y-%m-%d')
    #         except ValueError:
    #             raise ValidationError("Incorrect date format, should be DD-MM-YYYY")
    #     return super(Person, self).write(vals)
