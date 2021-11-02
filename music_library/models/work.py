# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Work(models.Model):
    _name = "work"
    _description = "A music work that may have multiple versions"
    
    active = fields.Boolean()

    oo_id = fields.Integer(default=-1)
    oo_genre = fields.Char()

    composer_id = fields.Many2one(comodel_name="composer", required=True)
    title = fields.Char(required=True)
    sub_title = fields.Char()
    nickname = fields.Char()
    name = fields.Char(compute="_compute_name")

    catalogue = fields.Char()
    catalogue_number = fields.Integer(default=False)
    catalogue_piece_number = fields.Integer(default=False)

    # Stored as a string because it's more convenient. Sometimes we have to write (1849-1852) because composer was lazy
    date = fields.Char()

    tonality_note = fields.Many2one(comodel_name="music.note")
    tonality_mode = fields.Selection(
        selection=[
            ('major', 'Major'),
            ('minor', 'Minor'),
        ],
        default="major"
    )

    is_popular = fields.Boolean(default=False)
    is_essential = fields.Boolean(default=False)

    @api.depends('title', 'composer_id')
    def _compute_name(self):
        for rec in self:
            rec.name = "%s: %s" % (rec.composer_id.name, rec.title)


    def action_update_tonality(self):
        # Todo: Change this for an action record?
        return {
            "name": _("Update tonality"),
            "type": 'ir.actions.act_window',
            "res_model": 'update.tonality.wizard',
            "views": [[False, "form"]],
            "target": 'new',
            "context": {
                **self.env.context,
                'default_work_ids': self.env.context.get('active_ids', []),
            },
        }

    def action_auto_fill_tonality(self):
        for note in self.env['music.note'].search([]):
            note_string = "%s%s" % (note.note, " "+note.alt if note.alt else "")
            note_string = "%s%s" % (note.note, " "+note.alt if note.alt else "")
            for mode in ['major', 'minor']:
                search_string = " in %s %s" % (note_string, mode[:3])
                works = self.env['work'].search([('tonality_note', '=', False), ('title', 'ilike', search_string)])
                works.write({'tonality_note': note.id, 'tonality_mode': mode})


