# patient model

from odoo import models, fields


class Patient(models.Model):
    _name = 'hr_hospital.patient'
    _inherit = 'hr_hospital.person'
    _description = 'Hospital Patients'

    personal_doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        string='Personal Doctor'
    )

    supervised_doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        string='Supervised Doctor'
    )

    disease_ids = fields.Many2many(
        comodel_name='hr_hospital.disease',
        string='Diseases'
    )

    visit_ids = fields.One2many(
        comodel_name='hr_hospital.visit',
        inverse_name='patient_id',
        string='Visits'
    )

    passport_info = fields.Char(
        string='Passport Information'
    )

    contact_person = fields.Char(
        string='Contact Person'
    )
    diagnosis_history = fields.One2many(
        comodel_name='hr_hospital.diagnosis',
        inverse_name='patient_id',
        string='Diagnosis History'
    )
    def action_view_visits(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Visits',
            'res_model': 'hr_hospital.visit',
            'view_mode': 'tree,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id}
        }

    def action_create_quick_visit(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Visit',
            'res_model': 'hr_hospital.visit',
            'view_mode': 'form',
            'context': {
                'default_patient_id': self.id,
                'default_doctor_id': self.personal_doctor_id.id if self.personal_doctor_id else False,
            },
            'target': 'new',
        }