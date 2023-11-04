from odoo import api, fields, models
from odoo.addons.music_library_api.utils.const import ApiAccess, SUCCESS_VALID_TOKEN, ERROR_TOKEN_INVALID, ERROR_NO_TOKEN
import string
from random import choice


class ApiToken(models.Model):
    _name = "api.token"
    _description = "A token used by a third-party app to access Octoopus api"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(required=True)
    access_token = fields.Char(copy=False, readonly=True, tracking=True)
    track_requests = fields.Boolean(default=False)
    request_ids = fields.One2many('api.request', 'token_id', string="Requests", copy=False)

    _sql_constraints = [
        ('unique_token', 'unique (access_token)', "This token already exists"),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ApiToken, self).create(vals_list)
        res.generate_new_token()
        return res


    def generate_new_token(self):
        for token in self:
            token.write({'access_token': "".join(choice(string.ascii_letters) for i in range(64))})

    def log_request(self, url: str, ip: str):
        for token in self:
            self.env['api.request'].sudo().create({
                'token_id': token.id,
                'url': url,
                'ip': ip,
            })

    @api.model
    def check_access(self, req) -> ApiAccess:
        # Todo: add some limits and check them here
        token = req.httprequest.headers.get('Authorization', None)
        if token is None:
            return ERROR_NO_TOKEN

        if token_id := self.search([('access_token', '=', token)]):
            if token_id.track_requests:
                token_id.log_request(req.httprequest.path, req.httprequest.remote_addr)
            return SUCCESS_VALID_TOKEN
        return ERROR_TOKEN_INVALID
