{
    'name': 'My super demo module',
    'version': '17.0.0.0.1',
    'summary': 'This is a demo module',


    'category': 'Customization',
    'author': 'Dmitriy Chumak, Odoo Community Association (OCA)',
    'website': 'https://dmitriy.chumak.com',

    'license': 'AGPL-3',
    'depends': [
        'base',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/my_demo_views.xml',
        ],

    'demo': [
        'demo/my_demo.xml'
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
    'external_dependencies': {

    },


    'images': ['static/description/icon.png'],
    'price': 0,
    'currency': 'EUR'
}
