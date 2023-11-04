import re

from odoo.http import content_disposition, Controller, request, route, Response
from odoo import api, fields, models, _
from collections import defaultdict
import werkzeug
import json
from odoo.addons.music_library_api.utils.api import check_access_token, ApiResponse
from odoo.addons.music_library_api.utils.misc import fill_str_date
from odoo.addons.music_library.utils.search import get_search_key, get_ensemble_search_key, generate_all_ensembles, categories_to_instruments, get_slot_by_type
from odoo.addons.music_library_api.utils.const import EXCLUDED_FIELDS, SUCCESS_VALID_TOKEN, ERROR_TOKEN_INVALID, ERROR_NO_TOKEN, ERROR_RECORD_DOES_NOT_EXIST
import logging
_logger = logging.getLogger(__name__)



# --------------------------------------------
#                   CONFIGURATION
# --------------------------------------------

# --- API Access & version
API_ROOT_URL = '/music/api'
API_VERSION = 'v1'

# --- Limit of records returned by API calls
API_LIMIT = 200



# --------------------------------------------
#            Do not modify below
# --------------------------------------------
API_URL = API_ROOT_URL + '/' + API_VERSION


# ------------- CONTROLLER CLASS FOR API ---------------- #
class ApiControllerV1(Controller):

    @staticmethod
    def search(model: str, domain):
        """
        Helper for ORM searches:
            - Call search with sudo()
            - Add is_api_published=True to the domain
            - Add limit and offset from request
        """
        domain = [('is_api_published', '=', True)] + domain
        offset = int(request.httprequest.args.get('offset', 0))
        return request.env[model].sudo().search(domain, limit=API_LIMIT, offset=offset)

    @staticmethod
    def browse(model: str, res_id: int):
        """
        Helper for ORM browse:
            - Call browse with sudo()
            - Add filtered on is_api_published=True
            - Add an exists() call at the end
        """
        return request.env[model].sudo().browse(res_id).filtered('is_api_published').exists()



    # --------------------------------------------
    #                   GENERAL
    # --------------------------------------------


    @check_access_token
    @route([API_URL + '/status'], type='json', auth="public", csrf=False)
    def status(self):
        return ApiResponse(message="Hello! I'm Octoopus API.").to_dict()


    # --------------------------------------------
    #                COMPOSERS
    # --------------------------------------------


    @check_access_token
    @route([API_URL + '/composers'], type='json', auth="public", csrf=False)
    def composers(self):
        """
        Return a list of composers
        It is possible to apply filters by passing parameters in the url:
            - name: str
            - date_from: str        (format: YYYY or YYYY-MM-DD)
            - date_to: str          (format: YYYY or YYYY-MM-DD)
            - country: str          (ISO code)
            - period_id: int
        """
        domain = []
        if name := request.httprequest.args.get('name'):
            domain += [('search_name', 'ilike', name)]
        if date_from := request.httprequest.args.get('date_from'):
            date_from = fill_str_date(date_from, year_start=True)
            domain += [('death', '>', date_from)]
        if date_to := request.httprequest.args.get('date_to'):
            date_to = fill_str_date(date_to, year_end=True)
            domain += [('birth', '<', date_to)]
        if country := request.httprequest.args.get('country'):
            domain += [('country_ids.code', '=', country)]
        if period_id := request.httprequest.args.get('period_id'):
            domain += [('period_id', '=', period_id)]

        composers = self.search('music.composer', domain)
        data = composers.get_music_api_data()
        return ApiResponse(data=data).to_dict()

    @check_access_token
    @route([API_URL + '/composer/<int:composer_id>'], type='json', auth="public", csrf=False)
    def composer(self, composer_id: int = 0):
        """ Return detailed info for a composer """
        if composer := self.browse('music.composer', composer_id):
            return ApiResponse(data=composer.get_music_api_data(detailed=True)[0]).to_dict()
        return ERROR_RECORD_DOES_NOT_EXIST.to_dict()



    @check_access_token
    @route([API_URL + '/composer/<int:composer_id>/works'], type='json', auth="public", csrf=False)
    def composer(self, composer_id: int = 0):
        """ Return the list of works for a composer, `is_api_published` is checked in get_music_api_data() """
        if composer := self.browse('music.composer', composer_id):
            return ApiResponse(data=composer.work_ids.get_music_api_data()).to_dict()
        return ERROR_RECORD_DOES_NOT_EXIST.to_dict()


    # --------------------------------------------
    #                   WORKS
    # --------------------------------------------


    @check_access_token
    @route([API_URL + '/works'], type='json', auth="public", csrf=False)
    def works(self):
        domain = []
        # Todo: add filters

        works = self.search('music.work', domain)
        res = works.to_music_api_data()

        return ApiResponse(data=res).to_dict()


    # @route(['/api/v1/composer/', '/api/v1/composer/<int:composer_id>'], type='json', auth="public", csrf=False)
    # def api_composer(self, composer_id: int = 0):
    #     """
    #     API Call for one or more composer by id
    #     In case of multiple records, the ids must be passed as an array in POST data (key=ids)
    #         :param composer_id: the id of the composer (used if call for 1 composer)
    #         :return: dict with composer infos (specific fields if 'fields' post data is passed)
    #     """
    #     post, _FIELDS, _RELATED_FIELDS = extract_post_data(request.httprequest.data)
    #
    #     # Access rights
    #     check = _check_api_access(request)
    #     if not check.get('success'):
    #         return check
    #
    #     # POST data has the priority
    #     ids = post.get('ids', [composer_id])
    #     composer = request.env['music.composer'].sudo().browse(ids)
    #     if not composer.exists():
    #         return ERROR_RECORD_DOES_NOT_EXIST
    #
    #     data = dict_result(composer, _FIELDS, _RELATED_FIELDS)
    #     return success_result(data)


    # @route(['/api/v1/composer/search'], type='json', auth="public", csrf=False)
    # def api_composer_search(self):
    #     """
    #     API Call to search for composers by str in name + others options like birth, etc...
    #     [POST] The following options are available:
    #         - 'fields': a list[] of field names to be returned
    #         - 'search': a str to filter composer's names
    #
    #     :return: list of dict with composer infos (specific fields if 'fields' post data is passed)
    #     """
    #     # Access rights
    #     check = _check_api_access(request)
    #     if not check.get('success'):
    #         return check
    #     # POST data
    #     post, _FIELDS, _RELATED_FIELDS = extract_post_data(request.httprequest.data)
    #
    #     # --- We start with an empty domain, then we apply filters
    #     domain = [('published', '=', bool(post.get('published', True)))]
    #
    #     if search := post.get('search'):
    #         domain.extend([('search_name', 'ilike', search)])
    #
    #     _logger.info("Search composers via api with domain: %s" % domain)
    #     try:
    #         composers = request.env['music.composer'].sudo().search(domain)
    #         data = dict_result(composers, _FIELDS, _RELATED_FIELDS)
    #         return success_result(data)
    #     except Exception as e:
    #         _logger.error("[%s] Error during API request: %s" % (type(e), e))


    # --------------------------------------------
    #                   WORKS
    # --------------------------------------------


    @route(['/api/v1/work/search'], type='json', auth="public", csrf=False)
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

    @route(['/api/v1/workversion/search'], type='json', auth="public", csrf=False)
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


        # ------------------------------------------------- Main informations for the search:
        instrument_slots = post.get('instrument_slots')
        # Temporary -> so I don't have to type instruments everytime. Todo: remove this part
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


    @route(['/api/v1/instrument/search'], type='json', auth="public", csrf=False)
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

        works = request.env['music.instrument'].sudo().search(domain)
        data = dict_result(works, _FIELDS, _RELATED_FIELDS)
        return success_result(data)


