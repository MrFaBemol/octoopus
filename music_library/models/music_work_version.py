# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class MusicWorkVersion(models.Model):
    _name = "music.work.version"
    _description = ""

    work_id = fields.Many2one(comodel_name="music.work")
