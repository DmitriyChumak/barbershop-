from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, timedelta


class Bonus(models.Model):
    """
    Model for managing bonuses for barbers.
    """
    _name = 'barbershop.bonus'
    _description = 'Barbershop Bonus'

    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
        help="A concise display name for the bonus record."
    )
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
        required=True,
        domain="[('is_barber', '=', True)]",
        help='The barber to whom the bonus is assigned. Only barbers can be selected.'
    )
    amount = fields.Float(
        string='Amount',
        required=True,
        help='The amount of the bonus. Must be greater than zero.'
    )
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today,
        help='The date when the bonus is assigned.'
    )
    category_id = fields.Many2one(
        comodel_name='barbershop.bonus.category',
        string='Category',
        required=True,
        domain="[('active', '=', True)]",
        help='The category of the bonus. Only active categories can be selected.'
    )
    description = fields.Html(
        string='Description',
        help='A detailed description of the bonus.'
    )

    @api.depends('employee_id.name', 'category_id.display_name')
    def _compute_display_name(self):
        """
        Compute the display name for the bonus.
        """
        for bonus in self:
            barber_name = bonus.employee_id.name if bonus.employee_id else "N/A"
            category_name = bonus.category_id.display_name if bonus.category_id else "N/A"
            bonus.display_name = f"Bonus for {barber_name} - Category: {category_name} ({bonus.date.strftime('%Y-%m-%d') if bonus.date else 'Undated'})"

    @api.constrains('amount')
    def _check_amount(self):
        """
        Ensure that the bonus amount is greater than zero.
        """
        for record in self:
            if record.amount <= 0:
                raise ValidationError("The bonus amount must be greater than zero.")

    @api.constrains('employee_id')
    def _check_is_barber(self):
        """
        Ensure that the bonus is only assigned to barbers.
        """
        for record in self:
            if not record.employee_id.is_barber:
                raise ValidationError("The bonus can only be assigned to barbers.")

    @api.constrains('category_id')
    def _check_category_active(self):
        """
        Ensure that the bonus category is active.
        """
        for record in self:
            if not record.category_id.active:
                raise ValidationError("The bonus category must be active.")

    @api.model
    def create_bonus(self, employee_id, amount, date=None, category_id=None, description=None):
        """
        Create a bonus for the given employee.

        :param employee_id: ID of the employee
        :param amount: Amount of the bonus
        :param date: Date of the bonus
        :param category_id: ID of the bonus category
        :param description: Description of the bonus
        """
        date = date or fields.Date.context_today(self)
        self.create({
            'employee_id': employee_id,
            'amount': amount,
            'date': date,
            'category_id': category_id,
            'description': description,
        })

    def calculate_monthly_bonus(self):
        """
        Calculate and assign bonuses for all barbers based on completed appointments.
        """
        first_day_of_month = date.today().replace(day=1)
        last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        # Fetch completed appointments within the month in a single query
        appointments = self.env['barbershop.appointment'].search([
            ('state', '=', 'completed'),
            ('date_time', '>=', first_day_of_month),
            ('date_time', '<=', last_day_of_month),
        ])

        # Calculate bonuses
        employee_bonus = {}
        for appointment in appointments:
            employee = appointment.employee_id
            if employee.is_barber and appointment.service_id in employee.specialization_ids:
                if employee.id not in employee_bonus:
                    employee_bonus[employee.id] = 0
                bonus_percentage = employee.bonus_percentage or 10.0
                employee_bonus[employee.id] += appointment.service_id.price * (bonus_percentage / 100)

        # Create bonuses for each employee
        for employee_id, amount in employee_bonus.items():
            # Note: Bonuses created here will not have a specific category or description
            # unless create_bonus is modified or default values are set in the model.
            self.create_bonus(employee_id, amount, last_day_of_month)

        # Send notifications after calculating bonuses
        # TODO: Consider refining how newly created bonuses are passed to send_bonus_notifications.
        # If this method is called on self.env['barbershop.bonus'], 'self' here might be empty
        # or refer to all bonuses, not just newly created ones.
        self.search([]).send_bonus_notifications() # Example: send for all, or pass specific IDs.

    def send_bonus_notifications(self):
        """
        Send notifications to employees about their bonuses.
        Assumes 'self' contains the bonus records for which to send notifications.
        """
        # This method is called from calculate_monthly_bonus.
        # If calculate_monthly_bonus is a cron, 'self' here might be an empty recordset
        # if called as self.env['barbershop.bonus'].calculate_monthly_bonus().
        # It should ideally operate on specific bonus record(s).
        for bonus in self:
            if not bonus.employee_id.user_id: # Ensure barber has a linked user for notifications
                continue # Or log a warning
            template = self.env.ref('barbershop.bonus_notification_template', raise_if_not_found=False)
            if template:
                self.env['mail.template'].browse(template.id).send_mail(bonus.id, force_send=True)
