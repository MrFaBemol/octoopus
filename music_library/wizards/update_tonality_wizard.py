# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class UpdateTonalityWizard(models.TransientModel):
    _name = "update.tonality.wizard"
    _description = "A wizard used to update tonality in batch"

    work_ids = fields.Many2many(comodel_name="work")

    tonality_note = fields.Many2one(comodel_name="music.note", required=True)
    tonality_mode = fields.Selection(
        selection=[
            ('major', 'Major'),
            ('minor', 'Minor'),
        ],
        default="major"
    )

    def action_update_tonality(self):
        self.work_ids.write({
            'tonality_note': self.tonality_note,
            'tonality_mode': self.tonality_mode,
        })

