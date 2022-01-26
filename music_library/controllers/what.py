# -*- coding: utf-8 -*-
import json

import werkzeug
import requests
from ..common.tools.oo_api import call
from odoo.http import content_disposition, Controller, request, route


class WhatController(Controller):

    @route(['/composer/<int:composer_id>'], type='http', auth="public", website=True)
    def what_composer(self, composer_id=0):
        post_data = {
            'fields': ['name', 'first_name', 'portrait_url'],
        }

        res = call(request, 'composer/%s' % composer_id, post_data)

        if not res['success']:
            return "<h3>Erreur</h1> %s " % res['error_message']
        else:
            data = res['data']
            data_count = res['data_count']
            return "<h3>BRAVO</h3> <br />  Nombre de résultats: %s <br/><br/> <img src='%s' /> <br/><br/> %s" % (data_count, data['portrait_url'], data)




    @route(['/what/composers'], type='http', auth="public", website=True)
    def what_search_composer(self, **get_data):
        post_data = {
            'fields': ['name', 'first_name', 'portrait_url'],
            'search': get_data.get('search', ""),
        }

        res = call(request, 'composer/search', post_data)

        if not res['success']:
            return "<h3>Erreur</h1> %s " % res['error_message']
        else:
            data = res['data']
            data_count = res['data_count']
            html = "<h3>BRAVO</h3> <br />  Nombre de résultats: %s <br/><br/> " % (data_count)
            for composer in data:
                html += "<br /><img src='%s' /> <br/> %s  <br/><br/><hr />" % (composer['portrait_url'], composer)

            return html



