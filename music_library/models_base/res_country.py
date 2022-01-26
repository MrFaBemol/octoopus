# -*- coding: utf-8 -*-
from random import randint
from odoo import fields, models


class ResCountry(models.Model):
    _inherit = "res.country"

    def _get_default_color(self):
        return randint(1, 11)

    color = fields.Integer(default=_get_default_color)
