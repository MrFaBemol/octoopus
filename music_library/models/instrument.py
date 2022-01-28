# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Instrument(models.Model):
    _name = "instrument"
    _description = "An instrument"

    name = fields.Char(required=True, translate=True)
    category_id = fields.Many2one(comodel_name="instrument.category", required=True)
    icon = fields.Binary()

    def _get_default_key(self):
        return self.env.ref('music_library.music_note_c').id or False

    key = fields.Many2one(comodel_name="music.note", required=True, default=_get_default_key)
    is_ensemble = fields.Boolean(related="category_id.is_ensemble_category", string="Is ensemble")
    is_accompaniment = fields.Boolean(related="category_id.is_accompaniment_category", string="Is accompaniment")
    accompanist_qty = fields.Integer()


    def name_get(self):
        res = []
        for instrument in self:
            res.append((instrument.id, instrument.name))
        return res