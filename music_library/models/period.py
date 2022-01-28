# -*- coding: utf-8 -*-
from random import randint

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Period(models.Model):
    _name = "period"
    _description = "A musical period defined by a start & an end date"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(required=True, translate=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date()
    date_display = fields.Char(compute="_compute_date_display")
    sequence = fields.Integer()
    color = fields.Integer(default=_get_default_color)

    @api.depends('date_start', 'date_end')
    def _compute_date_display(self):
        for period in self:
            period.date_display = "%s%s" % (period.date_start.year, (" - %s" % period.date_end.year) if period.date_end else "")

