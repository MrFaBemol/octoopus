# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MusicWorkVersionInstrument(models.Model):
    _name = "music.work.version.instrument"
    _description = "An instrument or an instrument category with a quantity for a work version"

    name = fields.Char(compute="_compute_name", store=True)
    work_version_id = fields.Many2one(comodel_name="music.work.version", required=True, ondelete="cascade")
    instrument_id = fields.Many2one(comodel_name="music.instrument", required=True, ondelete="restrict")
    quantity = fields.Integer(default=1)

    _sql_constraints = [
        ('check_quantity_gt_zero', 'CHECK(quantity > 0)', 'The instrument quantity should be greater than 0'),
    ]


    @api.depends('instrument_id', 'quantity')
    def _compute_name(self):
        for ins in self.filtered('instrument_id'):
            ins.name = "%s%s" % (
                "" if ins.quantity == 1 else str(ins.quantity) + " ",
                ins.instrument_id.name + ("*" if ins.instrument_id.is_category else "")
            )

