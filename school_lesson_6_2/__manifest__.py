{
    'name': 'School Lesson 6-2',
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
    'depends': [
        'base',
        'school_lesson_6_1',
    ],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/library_author_views.xml',
        'views/library_author_menu.xml',
        'views/library_book_views.xml',
        'data/library_author_data.xml',
    ],

    'i18n': [
        'uk_UA.po',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
