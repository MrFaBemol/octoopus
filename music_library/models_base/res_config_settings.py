from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    _description = "res.config.settings"

    module_music_library_api = fields.Boolean(string="Access music library data through an API")
    module_music_library_imslp = fields.Boolean(string="Use IMSLP api to fetch data")
    module_music_library_openopus = fields.Boolean(string="Use OpenOpus api to fetch data")
