# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class InstrumentCategory(models.Model):
    _name = "instrument.category"
    _description = "A category of instruments"
    _order = "sequence,id"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    parent_id = fields.Many2one(comodel_name="instrument.category")
    child_ids = fields.One2many(comodel_name="instrument.category", inverse_name="parent_id")
    is_ensemble_category = fields.Boolean(default=False)

    icon = fields.Binary()
    instrument_ids = fields.One2many(comodel_name="instrument", inverse_name="category_id")
    instrument_count = fields.Integer(compute="_compute_instrument_count")

    @api.depends('instrument_ids')
    def _compute_instrument_count(self):
        for rec in self:
            if rec.child_ids:
                rec.child_ids._compute_instrument_count()
            rec.instrument_count = len(rec.instrument_ids) + sum(rec.child_ids.mapped('instrument_count'))
