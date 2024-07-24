==================
School Lesson 6.3
==================

Overview
========

The `school_lesson_6_3` module extends the functionality of book categories in the library management system. It introduces the following features:

- Adds a button to the book category form view to show all books in the selected category.

Installation
============

To install this module, you need to:

1. Ensure that you have the `school_lesson_6_1` module installed and configured.
2. Install the `school_lesson_6_3` module from the Odoo Apps.

Configuration
=============

No additional configuration is needed for this module.

Usage
=====

1. Navigate to **Library > Book Categories**.
2. Select a book category.
3. Click on the **Show Books** button at the bottom of the form view to see all books in the selected category.

Models
======

- `library.book.category`: Inherits from the existing model in `school_lesson_6_1` and adds a method to get all books in the category.

Methods
=======

- `get_books`: Returns a list of all books that belong to the current category.

Dependencies
============

- `school_lesson_6_1`

Bug Tracker
===========

If you find any issues with this module, please report them on the project's issue tracker.

Credits
=======

Author: Dmitriy Chumak
Website: https://www.example.com
License: LGPL-3
