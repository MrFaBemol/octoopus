# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import string
from random import choice


class ApiToken(models.Model):
    _name = "api.token"
    _description = "A token used by a third-party app to access Octoopus api"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(required=True)
    token = fields.Char(copy=False, readonly=True, tracking=True)
    track_requests = fields.Boolean(default=False)

    _sql_constraints = [
        ('unique_token', 'unique (token)', "This token already exists"),
    ]

    @api.model
    def create(self, vals):
        res = super(ApiToken, self).create(vals)
        res.generate_new_token()
        return res


    def generate_new_token(self):
        for rec in self:
            rec.write({'token': "".join(choice(string.ascii_letters) for i in range(64))})

    def log_request(self, url: str, ip: str):
        for rec in self:
            self.env['api.request'].sudo().create({
                'token_id': rec.id,
                'url': url,
                'ip': ip,
            })


    def get_admin_token(self):
        # Todo: add security checks
        return self.env.ref('music_library.octoopus_standard_api_token').token

