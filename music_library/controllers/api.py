# -*- coding: utf-8 -*-
from ..common.tools import oo_api
import werkzeug
import json
from odoo.http import content_disposition, Controller, request, route, Response
from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

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

    # If the request comes directly from the server
    if headers.environ.get("HTTP_ORIGIN") == request.env['ir.config_parameter'].sudo().get_param('web.base.url'):
        return SUCCESS_VALID_TOKEN

    # Else we need a token (because it's an external request)
    if token := headers.get('oo-token'):
        if token_id := request.env['api.token'].sudo().search([('token', '=', token)]):
            if token_id.track_requests:
                token_id.log_request(request.httprequest.url, request.httprequest.remote_addr)
            return SUCCESS_VALID_TOKEN
        else:
            return ERROR_TOKEN_INVALID
    return ERROR_NO_TOKEN



def extract_post_data(data):
    post = json.loads(data)
    return post, post.get('fields', []), post.get('related_fields', {})




# Contains all the standard model fields (like create_date) and the useless mixin fields
EXCLUDED_FIELDS = {
    'activity_ids', 'active', 'has_message', 'website_message_ids', 'message_ids', '__last_update', 'message_unread_counter', 'create_uid',
    'message_unread', 'my_activity_date_deadline', 'activity_exception_icon', 'activity_type_id', 'message_needaction_counter', 'message_attachment_count',
    'activity_summary', 'message_main_attachment_id', 'message_is_follower', 'message_has_error_counter', 'write_uid', 'activity_state',
    'activity_exception_decoration', 'message_follower_ids', 'create_date', 'activity_date_deadline', 'activity_type_icon', 'message_needaction',
    'message_partner_ids', 'message_has_error', 'activity_user_id', 'message_has_sms_error'
}

def dict_result(records, returned_fields=None, related_fields=None):
    """
        Shortcut for Model.read() picking only a few fields
            :param records: Any records you want
            :param returned_fields: a set/list of field's names you need
            :param related_fields: a dict{} of list[] to get infos on related fields (override the id
            :return: A list[] of dict{}
    """
    res = []
    for rec in records:
        d = dict()
        if not returned_fields:
            returned_fields = set(rec._fields.keys()) - EXCLUDED_FIELDS

        for f in returned_fields:
            if isinstance(rec[f], models.BaseModel):
                data = rec[f].ids if f[-4:] == "_ids" else rec[f].id
                if rf := related_fields.get(f):
                    rf.append("id")
                    rf_res = dict_result(rec[f], set(rf))
                    data = rf_res if f[-4:] == "_ids" else rf_res[0]
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

    @route(['/api/composer/', '/api/composer/<int:composer_id>'], type='json', auth="public", website=True, csrf=False)
    def api_composer(self, composer_id=0):
        """
        API Call for one or more composer by id
        In case of multiple records, the ids must be passed as an array in POST data (key=ids)
            :param composer_id: the id of the composer (used if call for 1 composer)
            :return: dict with composer infos (specific fields if 'fields' post data is passed)
        """
        post, _FIELDS, _RELATED_FIELDS = extract_post_data(request.httprequest.data)

        # Access rights
        check = _check_api_access(request)
        if not check.get('success'):
            return check

        # POST data has the priority
        ids = post.get('ids', [composer_id])
        composer = request.env['composer'].sudo().browse(ids)
        if not composer.exists():
            return ERROR_RECORD_DOES_NOT_EXIST

        data = dict_result(composer, _FIELDS, _RELATED_FIELDS)
        return success_result(data)


    @route(['/api/composer/search'], type='json', auth="public", website=True, csrf=False)
    def api_composer_search(self):
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
        post, _FIELDS, _RELATED_FIELDS = extract_post_data(request.httprequest.data)

        # --- We start with an empty domain, then we apply filters
        domain = [('published', '=', bool(post.get('published', True)))]

        if search := post.get('search'):
            domain.extend([('search_name', 'ilike', search)])

        _logger.info("Search composers via api with domain: %s" % domain)
        composers = request.env['composer'].sudo().search(domain)
        data = dict_result(composers, _FIELDS, _RELATED_FIELDS)
        return success_result(data)

    # @route(['/api/work/<int:composer_id>'], type='json', auth="public", website=True, csrf=False)
    # def api_work(self, work_id=0):
    #     """
    #     API Call for precisely ONE work by id
    #         :param work_id: the id number of the work in database
    #         :return: dict with work infos (specific fields if 'fields' post data is passed)
    #     """
    #     # Access rights
    #     check = _check_api_access(request)
    #     if not check.get('success'):
    #         return check
    #     # POST data
    #     post, _FIELDS, _RELATED_FIELDS = extract_post_data(request.httprequest.data)
    #
    #     work = request.env['music.work'].sudo().browse(work_id)
    #     if not work.exists():
    #         return ERROR_RECORD_DOES_NOT_EXIST
    #
    #
    #     data = dict_result(work, _FIELDS, _RELATED_FIELDS)
    #     return success_result(data)


    @route(['/api/work/search'], type='json', auth="public", website=True, csrf=False)
    def api_work_search(self):
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
        post, _FIELDS, _RELATED_FIELDS = extract_post_data(request.httprequest.data)

        # --- We start with an empty domain, then we apply filters
        domain = []

        if search := post.get('search'):
            domain.extend(['|', '|', ('title', 'ilike', search), ('sub_title', 'ilike', search), ('nickname', 'ilike', search)])

        works = request.env['music.work'].sudo().search(domain)
        data = dict_result(works, _FIELDS, _RELATED_FIELDS)
        return success_result(data)
