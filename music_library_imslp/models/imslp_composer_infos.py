
from odoo import api, fields, models, _


class ImslpComposerInfos(models.Model):
    _name = "imslp.composer.infos"
    _description = "Some infos with key/value on an imslp composer"

    key = fields.Char(required=True)
    value = fields.Text()
    composer_id = fields.Many2one(comodel_name="imslp.composer", required=True)
