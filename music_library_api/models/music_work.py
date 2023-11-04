from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class MusicWork(models.Model):
    _name = "music.work"
    _inherit = ["music.work", "music.api.mixin"]

    # --------------------------------------------
    #                   API
    # --------------------------------------------

    @api.model
    def _get_music_api_returned_fields(self) -> list[str]:
        return [
            'composer_id',
            'title',
            'is_popular',
            'is_essential',
            'catalogue',

            'date_composition',
            'tonality_note',
            'tonality_mode',
            'version_qty',
        ]

    @api.model
    def _get_music_api_returned_fields_detailed(self) -> list[str]:
        return [
            'sub_title',
            'nickname',
            'name',
            'date_first_publication',
            'period_id',
            'duration',
            'dedication',
            'work_version_ids',
        ]

    @api.model
    def _get_music_api_related_fields(self) -> dict[str, list[str]]:
        return {
            'composer_id': ['full_name', 'display_name', 'slug_url'],
            'period_id': ['name'],
        }


