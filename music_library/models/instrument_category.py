# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class InstrumentCategory(models.Model):
    _name = "instrument.category"
    _description = "A category of instruments"
    _order = "sequence,id"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    parent_id = fields.Many2one(comodel_name="instrument.category")
    child_ids = fields.One2many(comodel_name="instrument.category", inverse_name="parent_id")
    is_ensemble_category = fields.Boolean(default=False, string="Is an ensemble")
    is_accompaniment_category = fields.Boolean(default=False, string="Is an accompaniment")

    icon = fields.Binary()
    instrument_ids = fields.One2many(comodel_name="instrument", inverse_name="category_id")
    all_instrument_ids = fields.Many2many(comodel_name="instrument", compute="_compute_all_instrument_ids")
    instrument_count = fields.Integer(compute="_compute_all_instrument_ids")


    @api.depends('child_ids', 'instrument_ids')
    def _compute_all_instrument_ids(self):
        for cat in self:
            if cat.child_ids:
                cat.child_ids._compute_all_instrument_ids()
            cat.all_instrument_ids = cat.child_ids.all_instrument_ids | cat.instrument_ids
            cat.instrument_count = len(cat.all_instrument_ids)

    # @api.depends('instrument_ids')
    # def _compute_instrument_count(self):
    #     for rec in self:
    #         if rec.child_ids:
    #             rec.child_ids._compute_instrument_count()
    #         rec.instrument_count = len(rec.instrument_ids) + sum(rec.child_ids.mapped('instrument_count'))
