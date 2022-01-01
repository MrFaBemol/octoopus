# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ApiRequest(models.Model):
    _name = "api.request"
    _description = "A tracked request"

    token_id = fields.Many2one(comodel_name="api.token", readonly=True)
    url = fields.Char(readonly=True)
    ip = fields.Char(readonly=True)