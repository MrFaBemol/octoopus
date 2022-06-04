# -*- coding: utf-8 -*-
from odoo import http, models, fields, _
from odoo.http import request, Controller, route
import werkzeug.utils

from odoo.addons.website.controllers.main import Website
# from music_library.common.tools.oo_api import call

class WhatController(Website):

    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        res = super(WhatController, self).index(**kw)
        return res

    """
        Composers
    """
    @route(['/what/composers'], type='http', auth="public", website=True)
    def what_composers(self):
        values = {}
        return request.render('website_still_alive.what_composers', values)

    @route(['/what/composer/<int:composer_id>'], type='http', auth="public", website=True)
    def what_composer_by_id(self, composer_id=0):
        composer = request.env['composer'].sudo().browse(composer_id).exists()
        return werkzeug.utils.redirect('/what/composer/%s' % composer.slug_url if composer else '')

    @route(['/what/composer/<int:composer_id>', '/what/composer/<model("composer"):composer>'], type='http', auth="public", website=True)
    def what_composer(self, composer_id=0, composer=None):
        values = {'composer': composer or request.env['composer'].sudo().browse(composer_id).exists()}
        return request.render('website_still_alive.what_composer', values)


    """
        Works
    """
    @route(['/what/works'], type='http', auth="public", website=True)
    def what_works(self):
        values = {}
        return request.render('website_still_alive.what_works', values)

