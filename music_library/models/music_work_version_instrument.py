# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class MusicWorkVersionInstrument(models.Model):
    _name = "music.work.version.instrument"
    _description = "An instrument or an instrument category with a quantity for a work version"

    name = fields.Char(compute="_compute_name", store=True)
    work_version_id = fields.Many2one(comodel_name="music.work.version", required=True, ondelete="cascade")
    instrument_id = fields.Many2one(comodel_name="instrument", ondelete="restrict")
    instrument_category_id = fields.Many2one(comodel_name="instrument.category", ondelete="restrict")
    quantity = fields.Integer(default=1)

    _sql_constraints = [
        ('check_quantity_gt_zero', 'CHECK(quantity > 0)', 'The instrument quantity should be greater than 0'),
    ]


    @api.depends('instrument_id', 'instrument_category_id', 'quantity')
    def _compute_name(self):
        for ins in self:
            ins.name = "%s%s" % (
                "" if ins.quantity == 1 else str(ins.quantity) + " ",
                ins.instrument_id.name or str(ins.instrument_category_id.name) + "*"
            )

    # def name_get(self):
    #     res = []
    #     for ins in self:
    #         res.append((ins.id, "%s%s" % (
    #             "" if ins.quantity == 1 else str(ins.quantity) + " ",
    #             ins.instrument_id.name or str(ins.instrument_category_id.name) + "*"
    #         )))
    #     return res

    @api.model
    def create(self, vals):
        instrument_id = vals.get('instrument_id', False)
        instrument_category_id = vals.get('instrument_category_id', False)
        if (not instrument_id and not instrument_category_id) or (instrument_id and instrument_category_id):
            raise UserError(_("You must choose either an instrument or a category"))
        if vals.get('quantity', 0) < 1:
            raise UserError(_("Quantity must be at least 1 for %s" % instrument_id if instrument_id else instrument_category_id))
        return super(MusicWorkVersionInstrument, self).create(vals)
