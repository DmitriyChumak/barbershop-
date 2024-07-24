"""
This module contains the models for the mydemo module.
"""

import logging

from odoo import (models, fields)

_logger = logging.getLogger(__name__)

class MyDemo(models.Model):
    """
       This is a demo model.
    """
    _name = 'my.demo'
    _description = 'mydemo'

    name = fields.Char()
    active = fields.Boolean(default=True)

    def name_get(self):
        """Return the display name of the record."""
        return [(record.id, record.name) for record in self]

    def action_do_something(self):
        """This is a demo action."""
        self.ensure_one()
