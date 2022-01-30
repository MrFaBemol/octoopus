# -*- coding: utf-8 -*-
from random import randint

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Period(models.Model):
    _name = "period"
    _description = "A musical period defined by a start & an end date"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(required=True, translate=True)
    description = fields.Char(translate=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date()
    date_display = fields.Char(compute="_compute_date_display")
    sequence = fields.Integer()
    color = fields.Integer(default=_get_default_color)

    composer_ids = fields.Many2many(comodel_name="composer", relation="composer_period_rel")
    composer_qty = fields.Integer(compute="_compute_composer_qty")

    @api.depends('date_start', 'date_end')
    def _compute_date_display(self):
        for rec in self:
            rec.date_display = "%s" % rec.date_start.year if rec.date_start else ""
            rec.date_display += (" - %s" % rec.date_end.year) if rec.date_end else ""

    @api.depends('composer_ids')
    def _compute_composer_qty(self):
        for rec in self:
            rec.composer_qty = len(rec.composer_ids)


    def action_open_composers_kanban(self):
        self.ensure_one()
        return {
            "name": _("All composers from %s period" % self.name),
            "type": 'ir.actions.act_window',
            "res_model": 'composer',
            "views": [[False, "kanban"], [False, "form"]],
            "target": 'self',
            "domain": [('id', 'in', self.composer_ids.ids)],
            "context": {
                **self.env.context,
            },
        }