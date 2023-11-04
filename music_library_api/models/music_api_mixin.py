from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons.music_library_api.utils.const import EXCLUDED_FIELDS
from typing import Any

import logging
_logger = logging.getLogger(__name__)


class MusicApiMixin(models.AbstractModel):
    _name = "music.api.mixin"
    _description = "music.api.mixin"

    is_api_published = fields.Boolean(default=False)


    @api.model
    def _get_music_api_returned_fields(self) -> list[str]:
        """ Return a list of fields names that should be returned by the api for this model """
        return []

    @api.model
    def _get_music_api_returned_fields_detailed(self) -> list[str]:
        """ Extend the list of fields names that should be returned by the api for this model, used with detailed=True option below """
        return []

    @api.model
    def _get_music_api_related_fields(self) -> dict[str, list[str]]:
        """
        Override to set default returned fields for relational fields (many2one, one2many, many2many) on API calls
        Example:
            return {
                'country_id': ['name', 'code'],
                'work_ids': ['name'],
            }
        """
        return {}

    @api.model
    def _get_music_api_ignored_fields(self) -> list[str]:
        """ Return a list of fields names that should be ignored by the api for this model """
        return []

    @api.model
    def _get_music_api_ignored_field_types(self) -> list[str]:
        """ Return a list of fields types that should be ignored by the api for this model """
        return []


    def get_music_api_data(self, detailed: bool = False) -> list[dict[str, Any]]:
        """ Called on a recordset to get data to send to the api """
        res = []
        for record in self.filtered('is_api_published'):
            res.append(record._get_music_api_data(detailed))
        return res


    def _get_music_api_data(self, detailed: bool = False) -> dict[str, Any]:
        """
            Called on a single record to get data to send to the api
                :param detailed: return more data (see _get_music_api_returned_fields_detailed())

                Relational fields don't return only ids but data and are handled this way:
                    - If the field is in _get_music_api_related_fields(), it will return the data of the related record
                    - Else, if the related model implements get_music_api_data(), it will be called (be careful of recursion)
                    - Else, it will be ignored (to avoid giving too much data)

                :return: dict
        """
        self.ensure_one()
        ignored_fields = set(self._get_music_api_ignored_fields())
        returned_fields = sorted(
            list(
                set(self._get_music_api_returned_fields() + (self._get_music_api_returned_fields_detailed() if detailed else []))
                - ignored_fields
                - EXCLUDED_FIELDS
            )
        )
        related_fields = self._get_music_api_related_fields() or dict()
        ignored_field_types = self._get_music_api_ignored_field_types()
        res = dict()

        for field_name in returned_fields:
            field_type = self._fields[field_name].type
            if field_type in ignored_field_types:
                continue

            if field_type in ("many2one", "one2many", "many2many"):
                if rel_field_names := related_fields.get(field_name):
                    rel_field_names = sorted(list(set(rel_field_names) | {"id"}))
                    data = self[field_name].read(rel_field_names)
                elif hasattr(self, f"get_music_api_data_{field_name}"):
                    # We don't propagate detailed param for related fields
                    data = getattr(self[field_name], f"get_music_api_data")()
                else:
                    continue

                # We want a dict for Many2one, and a list for One2many and Many2many
                if field_type == 'many2one':
                    data = data[0] if data else None

            else:
                data = self[field_name]

            res[field_name] = data

        return res





    # --------------------------------------------
    #                   ACTIONS
    # --------------------------------------------


    def action_api_publish(self):
        for record in self:
            record.is_api_published = True

    def action_api_unpublish(self):
        for record in self:
            record.is_api_published = False


