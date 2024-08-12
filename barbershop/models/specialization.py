from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Specialization(models.Model):
    """
    Model for managing barber specializations.
    """
    _name = 'barbershop.specialization'
    _description = 'Barbershop Specialization'

    name = fields.Char(
        string='Name',
        required=True,
        help='The name of the specialization or category.'
    )
    employee_ids = fields.Many2many(
        comodel_name='hr.employee',
        string='Barbers',
        domain="[('is_barber', '=', True)]",
        help='List of barbers who have this specialization.'
    )
    service_ids = fields.Many2many(
        comodel_name='barbershop.service',
        string='Services',
        help='List of services that are part of this specialization.'
    )
    create_date = fields.Datetime(
        string='Creation Date',
        readonly=True,
        help='The date and time when this record was created.'
    )
    write_date = fields.Datetime(
        string='Last Modification Date',
        readonly=True,
        help='The date and time when this record was last modified.'
    )
    barber_count = fields.Integer(
        string='Barber Count',
        compute='_compute_barber_count',
        store=True,
        help='The number of barbers associated with this specialization.'
    )
    service_count = fields.Integer(
        string='Service Count',
        compute='_compute_service_count',
        store=True,
        help='The number of services associated with this specialization.'
    )
    image = fields.Binary(
        string='Image',
        attachment=True,
        help='This field holds the image used as avatar for this specialization, limited to 1024x1024px.'
    )
    category_id = fields.Many2one(
        comodel_name='barbershop.specialization.category',
        string='Category',
        required=True,
        help='The category to which this specialization belongs.'
    )
    description = fields.Html(
        string='Description'
    )

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'The specialization name must be unique!')
    ]

    @api.constrains('name')
    def _check_name(self):
        """
        Ensure that the specialization name is at least 3 characters long.
        """
        for record in self:
            if len(record.name) < 3:
                raise ValidationError("The specialization name must be at least 3 characters long.")

    @api.depends('employee_ids')
    def _compute_barber_count(self):
        """
        Compute the number of barbers associated with the specialization.
        """
        for record in self:
            record.barber_count = len(record.employee_ids)

    @api.depends('service_ids')
    def _compute_service_count(self):
        """
        Compute the number of services associated with the specialization.
        """
        for record in self:
            record.service_count = len(record.service_ids)

    def unlink(self):
        """
        Prevent deletion of specialization if it is associated with barbers or services.
        """
        for record in self:
            if record.employee_ids or record.service_ids:
                raise ValidationError("You cannot delete a specialization that is associated with barbers or services.")
        return super(Specialization, self).unlink()
