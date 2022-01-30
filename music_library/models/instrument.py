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

    work_version_ids = fields.Many2many(comodel_name="music.work.version", relation="instrument_version_rel", compute="_compute_work_version_ids")
    work_version_qty = fields.Integer(compute="_compute_work_version_ids")


    def name_get(self):
        res = []
        for instrument in self:
            res.append((instrument.id, instrument.name))
        return res


    def _compute_work_version_ids(self):
        for rec in self:
            rec.work_version_ids = self.env['music.work.version.instrument'].search([('instrument_id', '=', rec.id)]).work_version_id.ids
            rec.work_version_qty = len(rec.work_version_ids)



    def action_open_versions_list(self):
        self.ensure_one()
        return {
            "name": _("All works versions for %s" % self.name),
            "type": 'ir.actions.act_window',
            "res_model": 'music.work.version',
            "views": [[False, "tree"], [False, "form"]],
            "target": 'self',
            "domain": [('id', 'in', self.work_version_ids.ids)],
            "context": {
                **self.env.context,
                'search_default_filter_group_by_composer_id': 0,
            },
        }
