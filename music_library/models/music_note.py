# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class MusicNote(models.Model):
    _name = "music.note"
    _description = "Music note used for keys/tonality/etc..."

    name = fields.Char(compute="_compute_name", store=True)

    note = fields.Selection(
        selection=[
            ('a', 'A'),
            ('b', 'B'),
            ('c', 'C'),
            ('d', 'D'),
            ('e', 'E'),
            ('f', 'F'),
            ('g', 'G'),
        ],
        default='a',
        required=True,
    )
    alt = fields.Selection(
        selection=[
            ('sharp', '#'),
            ('flat', '♭'),
        ],
    )

    def get_selection_label(self, obj, field_name, field_value):
        return _(dict(self.env[obj].fields_get(allfields=[field_name])[field_name]['selection'])[field_value])

    @api.depends('note', 'alt')
    def _compute_name(self):
        note_dict = {key: val for key, val in self._fields['note'].selection}
        alt_dict = {key: val for key, val in self._fields['alt'].selection}
        for rec in self:
            rec.name = note_dict[rec.note]
            rec.name += alt_dict[rec.alt] if rec.alt else ""
