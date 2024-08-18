{
    'name': 'Barber Shop Management',
    'version': '1.0',
    'summary': 'Module for managing a Barber Shop',
    'description': """
        The Barber Shop Management module is designed to help manage the operations of a barber shop. 
        It includes functionalities such as customer management, barber scheduling, service management, 
        appointment booking, and bonus calculation. Additionally, it provides reporting features to analyze 
        the shop's performance.
    """,
    'website': 'http://www.barbershop.com/',
    'author': 'Dmitriy Chumak',
    'category': 'Services/Barber Shop',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'contacts', 'hr', 'calendar'],
    'data': [
        'security/security_groups.xml',
        'security/security.xml',
        'security/ir.model.access.csv',

        'views/customer_views.xml',
        'views/barber_views.xml',
        'views/bonus_views.xml',
        'views/service_views.xml',
        'views/reminder_views.xml',
        'views/appointment_views.xml',
        'views/specialization_views.xml',
        'views/bonus_category_view.xml',
        'views/barber_holiday_views.xml',
        'views/barber_work_schedule_views.xml',
        'views/specialization_category.xml',
        'views/menu.xml',

        'data/bonus_mail_template_data.xml',
        'data/reminder_email_template_data.xml',
        'data/days_of_week.xml',

        'reports/report_barber_load_template.xml',

        'wizard/barber_load_report_wizard.xml',

    ],
    'demo': [
        'demo/specialization_category_demo.xml',
        'demo/specialization_demo.xml',
        'demo/service_demo.xml',
        'demo/bonus_category_demo.xml',
    ],
    'images': [
        'static/description/icon.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,

    'external_dependencies': {
        'python': ['matplotlib'],
    },
}
