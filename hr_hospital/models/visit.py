# visit model

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError, UserError
from odoo.tools.translate import _


class Visit(models.Model):
    _name = 'hr_hospital.visit'
    _description = 'Visit'

    name = fields.Char(
        string='Visit Name',
        compute='_compute_name',
        store=True
    )

    state = fields.Selection(
        selection=[
        ('planned', 'Planned'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ],
        string='Status',
        default='planned'
    )

    planned_date_time = fields.Datetime(
        string='Planned Date & Time'
    )

    actual_date_time = fields.Datetime(
        string='Actual Date & Time'
    )

    doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        string='Doctor',
        required=True
    )

    patient_id = fields.Many2one(
        comodel_name='hr_hospital.patient',
        string='Patient',
        required=True
    )

    diagnosis_ids = fields.One2many(
        comodel_name='hr_hospital.diagnosis',
        inverse_name='visit_id',
        string='Diagnoses'
    )

    symptoms = fields.Text(string='Symptoms')
    notes = fields.Text(string='Notes')

    visit_count = fields.Integer(
        string='Visit Count',
        compute='_compute_visit_count',
        store=True
    )

    # @api.depends("patient_id", planned_date_time)
    # def _compute_display_name(self):
    #     for visit in self:
    #         visit.name= f'{visit.patient_id.name} {visit.planned_date_time.strftime("%Y-%m")}'

    @api.depends('patient_id', 'planned_date_time')
    def _compute_name(self):
        for visit in self:
            visit.name = f'{visit.patient_id.name} - {visit.planned_date_time.strftime("%Y-%m-%d")}' \
                if visit.planned_date_time \
                else visit.patient_id.name

    @api.depends('doctor_id', 'planned_date_time')
    def _compute_visit_count(self):
        for visit in self:
            if visit.planned_date_time and visit.id:
                # the first day of the current month
                start_date = visit.planned_date_time.replace(day=1)

                # the last day of the current month
                next_month = start_date + timedelta(days=31)
                end_date = next_month.replace(day=1) - timedelta(days=1)

                visit_count = self.search_count([
                    ('doctor_id', '=', visit.doctor_id.id),
                    ('planned_date_time', '>=', start_date),
                    ('planned_date_time', '<=', end_date),
                    ('id', '!=', visit.id)
                ])
                visit.visit_count = visit_count + 1
            else:
                visit.visit_count = 1

    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'completed':
            self.actual_date_time = fields.Datetime.now()
            self.planned_date_time = self.actual_date_time
            self.doctor_id = self.doctor_id

    @api.constrains('planned_date_time', 'doctor_id', 'patient_id')
    def _check_visit_time(self):
        for visit in self:
            if visit.planned_date_time and visit.doctor_id and visit.patient_id:
                overlapping_visits = self.search([
                    ('doctor_id', '=', visit.doctor_id.id),
                    ('patient_id', '=', visit.patient_id.id),
                    ('planned_date_time', '=', visit.planned_date_time),
                    ('id', '!=', visit.id)
                ])
                if overlapping_visits:
                    raise ValidationError("The doctor already has an appointment with this patient on the same date.")

    @api.ondelete(at_uninstall=False)
    def _unlink_except_with_diagnosis(self):
        for visit in self:
            if visit.diagnosis_ids:
                raise UserError(_(
                    "You cannot delete a visit that has diagnoses associated with it."
                ))
