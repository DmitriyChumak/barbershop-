{
    'name': 'School Lesson 6-5',
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
        'school_lesson_6_1', 'school_lesson_6_2', 'school_lesson_6_3','school_lesson_6_4',
    ],
    'data': [
    ],

    'application': False,
    'installable': True,
    'auto_install': False,
}
