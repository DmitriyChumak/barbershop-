======================
School Lesson 6.5
======================

Overview
========

The `school_lesson_6_5` module is an integrated library management system that builds upon the functionalities provided by the previous modules `school_lesson_6_1`, `school_lesson_6_2`, `school_lesson_6_3`, and `school_lesson_6_4`. It provides comprehensive features for managing books, authors, categories, and user permissions within a library setting.

Features
========

- Manage authors and books.
- Categorize books into different categories.
- Set user permissions for library management.
- Provides a user-friendly interface for library operations.
- Adds a button to the book category form view to show all books in the selected category.

Installation
============

To install this module, you need to:

1. Ensure that you have the required modules installed and configured:
    - `school_lesson_6_1`
    - `school_lesson_6_2`
    - `school_lesson_6_3`
    - `school_lesson_6_4`
2. Install the `school_lesson_6_5` module from the Odoo Apps.

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

- `library.author`: Manages authors of books.
- `library.book`: Manages books and their attributes.
- `library.book.category`: Manages categories of books and includes a method to get all books in the category.
- `res.groups`: Manages user permissions and groups.

Methods
=======

- `library.author.get_books`: Returns a list of all books that belong to the current category.
- `library.book.action_scrap_book`: Marks a book as inactive.
- `res.users`: Manages user creation and permission assignments.

Dependencies
============

- `school_lesson_6_1`
- `school_lesson_6_2`
- `school_lesson_6_3`
- `school_lesson_6_4`

Bug Tracker
===========

If you find any issues with this module, please report them on the project's issue tracker.

Credits
=======

Author: Dmitriy Chumak
Website: https://www.example.com
License: LGPL-3
