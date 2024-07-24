from odoo import models, fields
from odoo.exceptions import UserError


class PersonalDoctor(models.TransientModel):
    _name = 'hr_hospital.personal.doctor.wizard'
    _description = 'Personal Doctor Wizard'

    name = fields.Char(string='Name')
    doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        string='Personal Doctor',
        required=True
    )
    patient_ids = fields.Many2many(
        comodel_name='hr_hospital.patient',
        string='Patients',
        relation='patient_personal_doctor_rel'
    )

    def assign_personal_doctor(self):
        self.ensure_one()
        if not self.patient_ids or not self.doctor_id:
            raise UserError("Please select both the patient and the doctor.")

        self.patient_ids.personal_doctor_id = self.doctor_id
        return {'type': 'ir.actions.act_window_close'}
