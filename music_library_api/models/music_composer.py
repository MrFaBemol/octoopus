from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons.music_library_api.utils.api import grant_access, call_api
import logging
_logger = logging.getLogger(__name__)

class MusicComposer(models.Model):
    _inherit = "music.composer"

    # --------------------------------------------
    #                   API
    # --------------------------------------------

    @grant_access
    def action_api_test(self):
        # Method here to do some tests
        post = {
            'fields': ['name', 'first_name', 'portrait_url'],
        }
        res = call_api(self, 'composer/34', post)
        print(res)
