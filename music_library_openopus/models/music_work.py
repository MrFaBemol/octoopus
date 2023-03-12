from odoo import fields, models
import logging
_logger = logging.getLogger(__name__)

class MusicWork(models.Model):
    _inherit = "music.work"

    oo_id = fields.Integer(default=-1)
    oo_genre = fields.Char()
