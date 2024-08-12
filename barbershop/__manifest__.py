{
    'name': 'Barber Shop',
    'version': '1.0',
    "summary": 'Module for managing Barber Shop',
    'website': 'http://www.barbershop.com/',
    'author': 'Dmitriy Chumak',
    'category': 'Uncategorized',
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
        # 'views/barber_break_views.xml', #I can delete it
        'views/barber_holiday_views.xml',
        'views/barber_work_schedule_views.xml',
        'views/specialization_category.xml',
        'views/menu.xml',

        'data/bonus_mail_template_data.xml',
        'data/reminder_email_template_data.xml',
        'data/days_of_week.xml',

        'reports/report_barber_load_template.xml',

    ],


    "demo": [
        'demo/specialization_category_demo.xml',
        'demo/specialization_demo.xml',
        'demo/service_demo.xml',
    ],
    'installable': True,
    'application': True,

    'external_dependencies': {

    },


}
