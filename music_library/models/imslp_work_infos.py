# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ImslpWorkInfos(models.Model):
    _name = "imslp.work.infos"
    _description = "Some infos with key/value on an imslp work"

    key = fields.Char(required=True)
    value = fields.Char()
    work_id = fields.Many2one(comodel_name="imslp.work", required=True)
