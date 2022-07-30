# -*- coding: utf-8 -*-
from odoo import fields, models
from ..common.datas import colors


class ResCountry(models.Model):
    _inherit = "res.country"

    color = fields.Integer(default=colors.get_odoo_default_color)
