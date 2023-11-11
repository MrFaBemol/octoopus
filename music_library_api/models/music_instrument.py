from odoo import api, models


class MusicInstrument(models.Model):
    _name = "music.instrument"
    _inherit = ["music.instrument", "music.api.mixin"]

    # --------------------------------------------
    #                   API
    # --------------------------------------------

    @api.model
    def _get_music_api_returned_fields(self) -> list[str]:
        return [
            'name',
            'display_name',
            'slug_url',
            'key_id',

            'is_category',
            'is_ensemble',
            'is_accompaniment',
            'accompanist_qty',
        ]

    @api.model
    def _get_music_api_returned_fields_detailed(self) -> list[str]:
        return [
            'extra_name_ids',
            'parent_id',
            'child_ids'
        ]

    @api.model
    def _get_music_api_related_fields(self) -> dict[str, list[str]]:
        return {
            'key_id': ['name', 'note', 'alt'],
            'extra_name_ids': ['name'],
            'parent_id': ['name'],
            'child_ids': ['name'],
        }


