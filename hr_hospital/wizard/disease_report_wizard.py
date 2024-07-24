from odoo import models, fields
from odoo.exceptions import UserError


class DiseaseReportWizard(models.TransientModel):
    _name = 'hr_hospital.disease.report.wizard'
    _description = 'Disease Report Wizard'

    start_date = fields.Date(
        string='Start Date',
        required=True
    )
    end_date = fields.Date(
        string='End Date',
    required=True
    )
    doctor_ids = fields.Many2many(
        comodel_name='hr_hospital.doctor',
        string='Doctors'
    )
    disease_ids = fields.Many2many(
        comodel_name='hr_hospital.disease',
        string='Diseases'
    )

    def generate_report(self):
        self.ensure_one()
        if self.start_date > self.end_date:
            raise UserError("The start date cannot be after the end date.")

        domain = [
            ('visit_id.planned_date_time', '>=', self.start_date),
            ('visit_id.planned_date_time', '<=', self.end_date)
        ]
        if self.doctor_ids:
            domain.append(('visit_id.doctor_id', 'in', self.doctor_ids.ids))
        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        diagnoses = self.env['hr_hospital.diagnosis'].search(domain)

        if not diagnoses:
            raise UserError("No diagnoses found for the given criteria.")

        report_data = self._prepare_report_data(diagnoses)
        self._display_report(report_data)

    def _prepare_report_data(self, diagnoses):
        report_data = []
        for diagnosis in diagnoses:
            data = {
                'patient_name': diagnosis.patient_id.name,
                'doctor_name': diagnosis.doctor_id.display_name,
                'disease_name': diagnosis.disease_id.name,
                'date': diagnosis.visit_id.planned_date_time,
            }
            report_data.append(data)
        return report_data

    def _display_report(self, report_data):
        report_message = ""
        for record in report_data:
            report_message += (
                f"Patient: {record['patient_name']}, "
                f"Doctor: {record['doctor_name']}, "
                f"Disease: {record['disease_name']}, "
                f"Date: {record['date']}\n"
            )

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Disease Report',
                'message': report_message,
                'sticky': False,
            }
        }