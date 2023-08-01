# -*- coding: utf-8 -*-
from odoo.http import request, route
from odoo.addons.website.controllers.main import Website


class OctoopusMain(Website):

    @route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        res = super(OctoopusMain, self).index(**kw)
        return res

