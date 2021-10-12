# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class MusicWork(models.Model):
    _name = "music.work"
    _description = "A music work that may have multiple versions"

    oo_id = fields.Integer(default=-1)
    oo_genre = fields.Char()

    composer_id = fields.Many2one(comodel_name="composer", required=True)
    title = fields.Char(required=True)
    sub_title = fields.Char()
    nickname = fields.Char()
    catalogue = fields.Char()
    catalogue_number = fields.Integer()

    # Stored as a string because it's more convenient. Sometimes we have to write (1849-1852) because composer was lazy
    date = fields.Char()

    tonality_key = fields.Selection(
        selection=[
            ('a', 'A'),
            ('b', 'B'),
            ('c', 'C'),
            ('d', 'D'),
            ('e', 'E'),
            ('f', 'F'),
            ('g', 'G'),
        ]
    )
    tonality_alt = fields.Selection(
        selection=[
            ('sharp', '#'),
            ('flat', '♭'),
        ]
    )
    tonality_mode = fields.Selection(
        selection=[
            ('major', 'Major'),
            ('minor', 'Minor'),
        ]
    )

    is_popular = fields.Boolean(default=False)
    is_essential = fields.Boolean(default=False)




