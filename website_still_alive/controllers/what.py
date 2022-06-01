# -*- coding: utf-8 -*-
from odoo import http, models, fields, _
from odoo.http import request, Controller, route

from odoo.addons.website.controllers.main import Website
# from music_library.common.tools.oo_api import call

class WhatController(Website):

    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        res = super(WhatController, self).index(**kw)
        return res


    @route(['/what/composers'], type='http', auth="public", website=True)
    def what_composers(self, **get_data):
        values = {}
        post_data = {
            'fields': ['name', 'first_name', 'portrait_url'],
            'search': get_data.get('search', ""),
        }

        res = {}
        # print(call(request, 'composer/search', post_data))
        return request.render('website_still_alive.what_composers', values)

        # res = call(request, 'composer/search', post_data)

        if not res.get('success'):
            return "<h3>Erreur</h1> %s " % res['error_message']
        else:
            data = res['data']
            data_count = res['data_count']
            html = "<h3>BRAVO</h3> <br />  Nombre de résultats: %s <br/><br/> " % (data_count)
            for composer in data:
                html += "<br /><img src='%s' /> <br/> %s  <br/><br/><hr />" % (composer['portrait_url'], composer)

            # return html

        return request.render('website_still_alive.testouille', values)

    @route(['/composer/<int:composer_id>'], type='http', auth="public", website=True)
    def what_composer(self, composer_id=0):
        post_data = {
            'fields': ['name', 'first_name', 'portrait_url'],
        }

        # res = call(request, 'composer/%s' % composer_id, post_data)
        res = {}

        if not res.get('success'):
            return "<h3>Erreur</h1> %s " % res['error_message']
        else:
            data = res['data']
            data_count = res['data_count']
            return "<h3>BRAVO</h3> <br />  Nombre de résultats: %s <br/><br/> <img src='%s' /> <br/><br/> %s" % (data_count, data['portrait_url'], data)
