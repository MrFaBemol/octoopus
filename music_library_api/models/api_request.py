from odoo import fields, models


class ApiRequest(models.Model):
    _name = "api.request"
    _description = "A tracked request"

    token_id = fields.Many2one(comodel_name="api.token", readonly=True, ondelete="cascade")
    url = fields.Char(readonly=True)
    ip = fields.Char(readonly=True)
