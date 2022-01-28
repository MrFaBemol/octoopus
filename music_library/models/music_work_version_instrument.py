# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class MusicWorkVersionInstrument(models.Model):
    _name = "music.work.version.instrument"
    _description = "An instrument or an instrument category with a quantity for a work version"

    work_version_id = fields.Many2one(comodel_name="music.work.version", required=True, ondelete="cascade")
    instrument_id = fields.Many2one(comodel_name="instrument", ondelete="cascade")
    instrument_category_id = fields.Many2one(comodel_name="instrument.category", ondelete="cascade")
    quantity = fields.Integer(default=1)

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, "%s%s" % ("" if rec.quantity == 1 else "%s " % rec.quantity, rec.instrument_id.name)))
        return res

    @api.model
    def create(self, vals):
        instrument_id = vals.get('instrument_id', False)
        instrument_category_id = vals.get('instrument_category_id', False)
        if (not instrument_id and not instrument_category_id) or (instrument_id and instrument_category_id):
            raise UserError(_("You must choose either an instrument or a category"))
        if vals.get('quantity', 0) < 1:
            raise UserError(_("Quantity must be at least 1 for %s" % instrument_id if instrument_id else instrument_category_id))
        return super(MusicWorkVersionInstrument, self).create(vals)
