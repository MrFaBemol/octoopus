# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Period(models.Model):
    _name = "period"
    _description = "A musical period defined by a start & an end date"
    
    name = fields.Char(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date()
