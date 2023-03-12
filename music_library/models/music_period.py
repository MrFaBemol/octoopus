# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from ..common.datas import colors



class MusicPeriod(models.Model):
    _name = "music.period"
    _description = "A musical period defined by a start & an end date"
    _order = "date_start"

    name = fields.Char(required=True, translate=True)
    description = fields.Char(translate=True)
    date_start = fields.Date()      # required in view
    date_end = fields.Date()
    date_display = fields.Char(compute="_compute_date_display")
    sequence = fields.Integer()
    color = fields.Integer(default=colors.get_odoo_default_color)
    color_material = fields.Char(compute="_compute_color_material")

    composer_ids = fields.Many2many(comodel_name="music.composer", relation="composer_period_rel")
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

    @api.depends('color')
    def _compute_color_material(self):
        for period in self:
            period.color_material = colors.MATERIAL_COLORS.get(period.color, colors.DEFAULT_MATERIAL_COLOR)


    def search_or_create_by_name(self, name: str, exact_match: bool = True):
        return self.search([('name', '=ilike' if exact_match else 'ilike', name)]) or self.create([{'name': name}])


    def action_open_composers_kanban(self):
        self.ensure_one()
        return {
            "name": _("All composers from %s period" % self.name),
            "type": 'ir.actions.act_window',
            "res_model": 'music.composer',
            "views": [[False, "kanban"], [False, "form"]],
            "target": 'current',
            "domain": [('id', 'in', self.composer_ids.ids)],
            "context": {
                **self.env.context,
            },
        }