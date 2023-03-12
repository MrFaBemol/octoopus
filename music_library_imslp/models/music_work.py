from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class MusicWork(models.Model):
    _inherit = "music.work"

    imslp_work_id = fields.Many2one(comodel_name="imslp.work")
