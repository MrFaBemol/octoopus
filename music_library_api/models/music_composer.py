from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
# from odoo.addons.music_library_api.utils.api import call_api
import logging
_logger = logging.getLogger(__name__)

class MusicComposer(models.Model):
    _name = "music.composer"
    _inherit = ["music.composer", "music.api.mixin"]

    # --------------------------------------------
    #                   API
    # --------------------------------------------

    @api.model
    def _get_music_api_returned_fields(self) -> list[str]:
        return [
            'full_name',
            'display_name',
            'search_name',
            'slug_url',
            'avatar_128',
            'birth',
            'death',
            'is_popular',
            'is_essential',
            'work_qty'
        ]

    @api.model
    def _get_music_api_returned_fields_detailed(self) -> list[str]:
        return [
            'name',
            'first_name',
            'period_id',
            'display_date',
            'portrait_url',
            'biography',
            'biography_short',
            'country_ids',
            'work_ids',
        ]

    @api.model
    def _get_music_api_related_fields(self) -> dict[str, list[str]]:
        return {
            'country_ids': ['name', 'code'],
            'period_id': ['name'],
            'work_ids': ['title'],
        }

