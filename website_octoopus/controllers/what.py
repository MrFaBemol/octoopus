# -*- coding: utf-8 -*-
from odoo import http, models, fields, _
from odoo.http import request, Controller, route
import werkzeug.utils
from odoo.addons.website.controllers.main import Website


class OctoopusWhat(Website):
    """
        Composers
    """
    # @route(['/what/composers'], type='http', auth="public", website=True)
    # def what_composers(self):
    #     values = {}
    #     return request.render('website_still_alive.what_composers', values)
    #
    # @route(['/what/composer/<int:composer_id>'], type='http', auth="public", website=True)
    # def what_composer_by_id(self, composer_id=0):
    #     """
    #     This controller only redirect with a proper url
    #         :param composer_id: int (id of composer in DB)
    #     """
    #     if composer := request.env['composer'].sudo().browse(composer_id).exists():
    #         return werkzeug.utils.redirect('/what/composer/%s' % composer.slug_url)
    #     return werkzeug.utils.redirect('/what/composers/')
    #
    # @route(['/what/composer/<model("composer"):composer>'], type='http', auth="public", website=True)
    # def what_composer(self, composer=None):
    #     if not composer.published:
    #         return werkzeug.utils.redirect('/what/composers/')
    #     values = {'composer': composer}
    #     return request.render('website_still_alive.what_composer', values)


    """
        Works
    """
    # @route(['/what/works'], type='http', auth="public", website=True)
    # def what_works(self):
    #     values = {}
    #     return request.render('website_still_alive.what_works', values)

