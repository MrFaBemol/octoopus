# -*- coding: utf-8 -*-
from ..common.tools import oo_api
import werkzeug
import json
from odoo.http import content_disposition, Controller, request, route, Response


# Some success / error messages
SUCCESS_VALID_TOKEN = {
    'success': True
}
ERROR_TOKEN_INVALID = {
    'success': False,
    'error_message': "Access denied: your token is invalid.",
}
ERROR_NO_TOKEN = {
    'success': False,
    'error_message': "Access denied: you need to pass a valid token in the POST data to access API",
}
ERROR_RECORD_DOES_NOT_EXIST = {
    'success': False,
    'error_message': "Error: this record doesn't exist",
}


def _check_api_access(request):
    """
        Check if the request is made using a valid API token and log the request if needed
            :param request: the request
            :return: a dict with success status and an error message if needed
    """
    headers = request.httprequest.headers
    if token := headers.get('oo-token'):
        if token_id := request.env['api.token'].sudo().search([('token', '=', token)]):
            if token_id.track_requests:
                token_id.log_request(request.httprequest.url, request.httprequest.remote_addr)
            return SUCCESS_VALID_TOKEN
        else:
            return ERROR_TOKEN_INVALID
    return ERROR_NO_TOKEN




# Contains all the standard model fields (like create_date) and the useless mixin fields
EXCLUDED_FIELDS = {
    'activity_ids', 'active', 'has_message', 'website_message_ids', 'message_ids', '__last_update', 'message_unread_counter', 'create_uid',
    'message_unread', 'my_activity_date_deadline', 'activity_exception_icon', 'activity_type_id', 'message_needaction_counter', 'message_attachment_count',
    'activity_summary', 'message_main_attachment_id', 'message_is_follower', 'message_has_error_counter', 'write_uid', 'activity_state',
    'activity_exception_decoration', 'message_follower_ids', 'create_date', 'activity_date_deadline', 'activity_type_icon', 'message_needaction',
    'message_partner_ids', 'message_has_error', 'activity_user_id', 'message_has_sms_error'
}

def dict_result(records, returned_fields=None):
    """
        Shortcut for Model.read() picking only a few fields
            :param records: Any records you want
            :param returned_fields: a set/list of field's names you need
            :return: A list[] of dict{}
    """
    res = []
    for rec in records:
        d = dict()
        if not returned_fields:
            returned_fields = set(rec._fields.keys()) - EXCLUDED_FIELDS
        for f in returned_fields:
            if f not in ['id', 'oo_id'] and f[-3:] == "_id":
                data = rec[f].id
            elif f[-4:] == "_ids":
                data = rec[f].ids
            else:
                data = rec[f]
            d[f] = data
        res.append(d)
    return res

def success_result(data):
    return {
        'success': True,
        'data': data,
        'data_count': len(data) if isinstance(data, list) else 1
    }


# ------------- CONTROLLER CLASS FOR API ---------------- #
class ApiController(Controller):

    @route(['/api/composer/<int:composer_id>'], type='json', auth="public", website=True, csrf=False)
    def api_composer(self, composer_id=0):
        """
        API Call for precisely ONE composer by id
            :param composer_id: the id number of the composer in database
            :return: dict with composer infos (specific fields if 'fields' post data is passed)
        """
        post = json.loads(request.httprequest.data)
        _FIELDS = post.get('fields', [])

        # Access rights
        check = _check_api_access(request)
        if not check.get('success'):
            return check

        composer = request.env['composer'].sudo().browse(composer_id)
        if not composer.exists():
            return ERROR_RECORD_DOES_NOT_EXIST

        # We return a dict here, as there is only one composer by id
        data = dict_result(composer, _FIELDS)[0]
        return success_result(data)


    @route(['/api/composer/search'], type='json', auth="public", website=True, csrf=False)
    def api_search_composer(self):
        """
        API Call to search for composers by str in name + others options like birth, etc...
        [POST] The following options are available:
            - 'fields': a list[] of field names to be returned
            - 'search': a str to filter composer's names

        :return: list of dict with composer infos (specific fields if 'fields' post data is passed)
        """
        # Access rights
        check = _check_api_access(request)
        if not check.get('success'):
            return check
        # POST data
        post = json.loads(request.httprequest.data)
        _FIELDS = post.get('fields', [])

        # --- We start with all the composers, then we apply filters
        result_composers = request.env['composer'].sudo().search([])

        if search := post.get('search'):
            result_composers = result_composers.search(['|', ('name', 'ilike', search), ('first_name', 'ilike', search)])

        data = dict_result(result_composers, _FIELDS)
        return success_result(data)


