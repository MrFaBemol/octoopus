# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class InstrumentExtraName(models.Model):
    _name = "instrument.extra.name"
    _description = "A name used when searching for instrument"

    name = fields.Char(required=True)
    instrument_id = fields.Many2one(comodel_name="instrument", required=True)
