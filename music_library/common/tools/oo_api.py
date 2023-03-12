# -*- coding: utf-8 -*-
from odoo import _
from odoo.exceptions import UserError, ValidationError
import requests
import json
import werkzeug


def grant_access(f):
    """
        A decorator to add before a method to grant access to api
        Not sure if useful............
    """
    def _grant_access(*self, **kwargs):
        f(self[0].with_context(grant_api_access=True), **kwargs)
    return _grant_access

def call_api(self, url: str, post_data: dict = None) -> dict:
    """
        This method allows a user to call the api in a python method (using the @grant_access decorator)
        Not very useful for now, but can be used to check what API returns, simulate a behaviour, etc...

        :param self: The recordset, mainly used to get access to env (& etc...)
        :param url: The url to call (ex: "composer/34")
        :param post_data: A dict{} with post data

        :return: a dict{} with api result
    """
    if self.env.context.get('grant_api_access', False):
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
