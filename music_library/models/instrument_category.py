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

    work_version_ids = fields.Many2many(comodel_name="music.work.version", relation="instrument_category_version_rel", compute="_compute_work_version_ids")
    work_version_qty = fields.Integer(compute="_compute_work_version_ids")


    @api.depends('child_ids', 'instrument_ids')
    def _compute_all_instrument_ids(self):
        for cat in self:
            if cat.child_ids:
                cat.child_ids._compute_all_instrument_ids()
            cat.all_instrument_ids = cat.child_ids.all_instrument_ids | cat.instrument_ids
            cat.instrument_count = len(cat.all_instrument_ids)


    def _compute_work_version_ids(self):
        for rec in self:
            rec.work_version_ids = self.env['music.work.version.instrument'].search([('instrument_id', 'in', rec.all_instrument_ids.ids)]).work_version_id.ids
            rec.work_version_qty = len(rec.work_version_ids)


    def write(self, vals):
        res = super(InstrumentCategory, self).write(vals)
        if 'name' in vals:
            self.env['music.work.version.instrument'].search([('instrument_category_id', 'in', self.ids)])._compute_name()
        return res


    def get_from_string(self, string, check_plural=True):
        category = self.search([('name', '=ilike', string)]).exists()
        if not category and check_plural:
            pl_string = string[:-1] if string[-1].lower() == "s" else string+"s"
            category = self.search([('name', '=ilike', pl_string)]).exists()
        return category

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