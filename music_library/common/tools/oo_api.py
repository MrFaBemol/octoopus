# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from odoo import _
from odoo.exceptions import UserError, ValidationError
import requests
import json
import werkzeug


def grant_access(f):
    def _grant_access(*self, **kwargs):
        f(self[0].with_context(grant_api_access=True), **kwargs)
    return _grant_access

def call(self, url, post_data=None):
    # Todo: stop using LocalProxy, instead always call
    if self.env.context.get('grant_api_access', False) or type(self) == werkzeug.local.LocalProxy:
        url = self.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/api/' + url
        headers = {
            'oo-token': self.env['api.token'].get_admin_token(),
            'content-type': 'application/json'
        }
        res = requests.post(
            url,
            data=json.dumps(post_data or {}),
            headers=headers,
        )
        return res.json()['result']
    else:
        raise UserError(_("Request denied.\nIf you try to access Octoopus API from python code, please use @grant_access decorator."))
