# -*- coding: utf-8 -*-
from odoo import fields, models


class MusicInstrumentExtraName(models.Model):
    _name = "music.instrument.extra.name"
    _description = "A name used when searching for instrument"

    name = fields.Char(required=True)
    instrument_id = fields.Many2one(comodel_name="music.instrument", required=True)
