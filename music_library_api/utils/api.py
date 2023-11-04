from odoo.http import content_disposition, Controller, request, route, Response
from odoo import _
from odoo.exceptions import UserError, ValidationError
import requests
import json
import werkzeug
from typing import Union



class ApiAccess:
    def __init__(self, success: bool, message: str):
        self.success = success
        self.message = message



class ApiResponse:
    def __init__(self, success: bool = True, status_code: int = 200, message: str = None, data: Union[list, dict] = None):
        self.success = success
        self.status_code = status_code
        self.message = message or ("OK" if success else "NOK")
        self.data = data or {}


    def to_dict(self) -> dict:
        res = {
            'success': self.success,
            'status_code': self.status_code,
            'message': self.message,
            'data': self.data,
        }
        if isinstance(self.data, list):
            res['data_count'] = len(self.data)

        return res

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_response(self) -> Response:
        return Response(
            status=200,
            headers={
                'Content-Type': 'application/json',
            },
            response=self.to_json(),
        )



def check_access_token(fn):
    def _check_access_token(self, *args, **kwargs):
        access = request.env['api.token'].sudo().check_access(request)
        if access.success is not True:
            return {'success': False, 'message': access.message or "Access denied: unknown error."}

        res = fn(self, *args, **kwargs)
        # Todo: log the result maybe?
        return res
    if hasattr(fn, 'original_routing'):
        _check_access_token.original_routing = fn.original_routing
    return _check_access_token








# def call_api(self, url: str, post_data: dict = None) -> dict:
#     """
#         This method allows a user to call the api in a python method (using the @grant_access decorator)
#         Not very useful for now, but can be used to check what API returns, simulate a behaviour, etc...
#
#         :param self: The recordset, mainly used to get access to env (& etc...)
#         :param url: The url to call (ex: "composer/34")
#         :param post_data: A dict{} with post data
#
#         :return: a dict{} with api result
#     """
#     if self.env.context.get('grant_api_access', False):
#         url = self.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/api/v1' + url
#         headers = {
#             'oo-token': self.env['api.token'].get_admin_token(),
#             'content-type': 'application/json'
#         }
#         res = requests.post(
#             url,
#             data=json.dumps(post_data or {}),
#             headers=headers,
#         )
#         return res.json()['result']
#     else:
#         raise UserError(_("Request denied.\nIf you try to access Octoopus API from python code, please use @grant_access decorator."))
