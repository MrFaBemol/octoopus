from odoo import fields, models
from odoo.addons.music_library.utils import colors


class ResCountry(models.Model):
    _inherit = "res.country"

    color = fields.Integer(default=colors.get_odoo_default_color)
