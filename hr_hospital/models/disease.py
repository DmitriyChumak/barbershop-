# desease model

from odoo import models, fields, api


class Disease(models.Model):
    _name = 'hr_hospital.disease'
    _description = 'Disease'
    _parent_store = True
    _parent_name = 'parent_id'

    name = fields.Char(
        string='Name',
        required=True
    )

    code = fields.Char(
        string='Code',
        required=True
    )

    description = fields.Text(
        string='Description'
    )

    parent_id = fields.Many2one(
        comodel_name='hr_hospital.disease',
        string='Parent Disease',
        index=True,
        ondelete='restrict'
    )

    child_ids = fields.One2many(
        comodel_name='hr_hospital.disease',
        inverse_name='parent_id',
        string='Child Diseases'
    )

    parent_path = fields.Char(
        index=True,
        unaccent=False
    )

    complete_name = fields.Char(
        string='Complete Name',
        compute='_compute_complete_name',
        store=True,
        recursive=True
    )

    parent_left = fields.Integer(index=True)
    parent_right = fields.Integer(index=True)

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for disease in self:
            if disease.parent_id:
                disease.complete_name = f'{disease.parent_id.complete_name} / {disease.name}'
            else:
                disease.complete_name = disease.name

    sql_constraints = [
        ('name_uniq', 'unique (name)', "Disease name already exists!"),
        ('code_uniq', 'unique (code)', "Disease code already exists!"),
    ]

    def name_get(self):
        res = []
        for disease in self:
            names = []
            current = disease
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((disease.id, ' / '.join(reversed(names))))
        return res
