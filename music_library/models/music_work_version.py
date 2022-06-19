# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


# Todo: Add a genre model

class MusicWorkVersion(models.Model):
    _name = "music.work.version"
    _description = "Version of a music work (can be original or arrangement)"
    _inherits = {'music.work': 'work_id'}
    _order = "title"

    active = fields.Boolean(default=True)

    # Essential infos
    work_id = fields.Many2one(comodel_name="music.work", readonly=True, required=True, ondelete='cascade')
    instrument_ids = fields.One2many(comodel_name="music.work.version.instrument", inverse_name="work_version_id", string="Instruments")
    soloist_qty = fields.Integer(compute="_compute_performer_qty", string="Soloists", store=True)
    accompanist_qty = fields.Integer(compute="_compute_performer_qty", string="Accompanists", store=True)

    is_original = fields.Boolean(default=True)
    arranger_id = fields.Many2one(comodel_name="composer", ondelete="set null")

    # Alt infos (optional)
    alt_name = fields.Char(translate=True)
    alt_catalogue = fields.Char(translate=True)
    alt_catalogue_number = fields.Integer()
    alt_catalogue_piece_number = fields.Integer()
    alt_date = fields.Char()
    alt_tonality_note = fields.Many2one(comodel_name="music.note")
    alt_tonality_mode = fields.Selection(
        selection=[
            ('major', 'Major'),
            ('minor', 'Minor'),
        ],
        default="major"
    )

    # TODO: ajouter une action pour voir les infos d'imslp depuis la vue de ce modèle

    @api.depends('instrument_ids')
    def _compute_performer_qty(self):
        for version in self:
            instruments = version.instrument_ids.filtered(lambda i: not i.instrument_id.is_ensemble)
            accompanists = instruments.filtered('instrument_id.is_accompaniment')
            soloists = instruments - accompanists
            version.soloist_qty = sum(soloists.mapped('quantity'))
            version.accompanist_qty = sum([a.quantity*a.instrument_id.accompanist_qty for a in accompanists])


