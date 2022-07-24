# -*- coding: utf-8 -*-
from odoo.http import content_disposition, Controller, request, route, Response
from odoo import api, fields, models, _
from collections import defaultdict
import werkzeug
import json
from ..common.tools import oo_api
from ..common.tools.search import get_search_key, get_ensemble_search_key, generate_all_ensembles, categories_to_instruments, get_slot_by_type
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
ERROR_MISSING_POST_DATA = {
    'success': False,
    'error_message': "Error: your request misses required post data",
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
            :param related_fields: a dict{} of list[] to get infos on related fields (override the id, so result is a dict instead of int)
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

    # --------------------------------------------
    #                COMPOSERS
    # --------------------------------------------

    @route(['/api/composer/', '/api/composer/<int:composer_id>'], type='json', auth="public", csrf=False)
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


    @route(['/api/composer/search'], type='json', auth="public", csrf=False)
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
        try:
            composers = request.env['composer'].sudo().search(domain)
            data = dict_result(composers, _FIELDS, _RELATED_FIELDS)
            return success_result(data)
        except Exception as e:
            _logger.error("[%s] Error during API request: %s" % (type(e), e))


    # --------------------------------------------
    #                   WORKS
    # --------------------------------------------

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


    @route(['/api/work/search'], type='json', auth="public", csrf=False)
    def api_work_search(self):
        """
        API Call to search for works by str in name + others options like period, etc...
        [POST] The following options are available:
            - 'fields': a list[] of field names to be returned
            - 'search': a str to filter works names

        :return: list of dict with works infos (specific fields if 'fields' post data is passed)
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

    @route(['/api/workversion/search'], type='json', auth="public", csrf=False)
    def api_workversion_search(self):
        """
        API Call to search for works by instrumentation
        [POST] The following options are available:
            - 'fields': a list[] of field names to be returned
            - 'instrument_qty': int
            - 'instrument_slots': a list[] of list[]

        :return: list of dict with works infos (specific fields if 'fields' post data is passed)
        """
        # Access rights
        check = _check_api_access(request)
        if not check.get('success'):
            return check
        # POST data
        post, _FIELDS, _RELATED_FIELDS = extract_post_data(request.httprequest.data)

        print("=====================================================")
        print("jhjkj")

        # ------------------------------------------------- Main informations for the search:
        instrument_slots = post.get('instrument_slots')
        # 252: bowed, 254: strings, 251 : keyboards, 198, 199
        instrument_slots = [[251, 203]]
        if not instrument_slots:
            return ERROR_MISSING_POST_DATA
        min_soloists_qty = max(post.get('min_soloists_qty', 0), len(instrument_slots))
        max_soloists_qty = max(min_soloists_qty, post.get('max_soloists_qty', len(instrument_slots)))

        # First, we create a domain for the initial search
        domain = [
            ('soloist_qty', '>=', min_soloists_qty),
            ('soloist_qty', '<=', max_soloists_qty),
        ]




        # ------------------------------------------------- The main request
        res = request.env['music.work.version']
        work_version_with_domain = request.env['music.work.version'].search(domain)


        # Recast to int
        instrument_slots = [[int(i_id) for i_id in slot] for slot in instrument_slots]
        # Replace categories by the all_instrument_ids field
        instrument_slots = categories_to_instruments(request, instrument_slots)
        # Separate slots in fixed/variable
        fixed_slots, variable_slots = get_slot_by_type(instrument_slots)
        fixed_ensemble = defaultdict(int)
        for slot in fixed_slots:
            fixed_ensemble[slot[0]] += 1

        # Finally the search key!
        search_key = get_search_key(instrument_slots, min_instrument_qty=min_soloists_qty, max_instrument_qty=max_soloists_qty)

        # print(search_key)
        # print(fixed_slots)
        # print(fixed_ensemble)
        # print(variable_slots)
        # print(generate_all_ensembles(variable_slots))
        # print("=====================================================")

        """
        This is the common recordset from which we will start the filtering
        We filter on instrument_ids which has to validate all fixed slots
        """
        fixed_slots_works = work_version_with_domain.filtered(
            lambda v: all([v.instrument_ids.filtered(
                lambda i: i_id in i.instrument_id.get_all_ids() and i.quantity >= qty
            ) for i_id, qty in fixed_ensemble.items()])
        )

        """
        Here we search for works by ensemble, starting from the fixed_slots_works
        """
        works_by_ensemble = dict()

        for ensemble in generate_all_ensembles(variable_slots):
            # Start from fixed ensemble and add variable instruments -> dict
            complete_ensemble = fixed_ensemble.copy()
            for ins_id, qty in ensemble.items():
                complete_ensemble[ins_id] += qty

            ensemble_key = get_ensemble_search_key(complete_ensemble)

            works_by_ensemble[ensemble_key] = fixed_slots_works.filtered(
                lambda v: all([v.instrument_ids.filtered(
                    lambda i: i_id in i.instrument_id.get_all_ids() and i.quantity >= qty + fixed_ensemble.get(i_id, 0)
                ) for i_id, qty in ensemble.items()])
            )

        for k, w in works_by_ensemble.items():
            print(k)
            print(w.mapped('name'))
            print(len(w.mapped('name')))




        print("=====================================================")
        data = {}
        return success_result(data)



    # --------------------------------------------
    #                INSTRUMENTS
    # --------------------------------------------


    @route(['/api/instrument/search'], type='json', auth="public", csrf=False)
    def api_instrument_search(self):
        """
        API Call to search for instruments
        [POST] The following options are available:
            - 'fields': a list[] of field names to be returned
            - 'search': a str to filter instrument's names

        :return: list of dict with instruments infos (specific fields if 'fields' post data is passed)
        """
        # Access rights
        check = _check_api_access(request)
        if not check.get('success'):
            return check
        # POST data
        post, _FIELDS, _RELATED_FIELDS = extract_post_data(request.httprequest.data)

        # --- We start with an empty domain, then we apply filters
        domain = []

        # Todo: add key, etc......
        if search := post.get('search'):
            domain.extend([('name', 'ilike', search)])
        if post.get('ignore_all_category', True):
            domain.extend([('id', '!=', request.env.ref('music_library.instrument_all').id)])
        if post.get('ignore_accompaniment', True):
            domain.extend([('is_accompaniment', '=', False)])
        if post.get('ignore_category', False):
            domain.extend([('is_category', '=', False)])

        works = request.env['instrument'].sudo().search(domain)
        data = dict_result(works, _FIELDS, _RELATED_FIELDS)
        return success_result(data)


