# -*- coding: utf-8 -*-
{
    'name': 'School Lesson 6-1',
    'version': '1.0',
    'category': 'Library',
    'summary': 'Manage library books and categories',
    'description': """
        Library Management Module
        =========================

        This module provides functionalities to manage books and book categories
        in a library. You can create, edit, and delete books and categories, and 
        track which user has checked out a book.
    """,
    'author': 'Dmitriy Chumak',
    'website': 'http://www.example.com',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
        'views/library_book_category_views.xml',
        'views/library_menu.xml',
        'data/library_book_category_data.xml',

    ],
    'demo': [
        'demo/library_book_demo.xml',
        'demo/library_book_update_demo.xml',
    ],

    'i18n': [
        'uk_UA.po',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
