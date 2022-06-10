# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class MusicWork(models.Model):
    _name = "music.work"
    _description = "A music work that may have multiple versions"
    _order = "title"
    
    active = fields.Boolean(default=True)

    oo_id = fields.Integer(default=-1)
    oo_genre = fields.Char()

    composer_id = fields.Many2one(comodel_name="composer", required=True, ondelete='restrict')
    title = fields.Char(required=True, translate=True)
    sub_title = fields.Char(translate=True)
    nickname = fields.Char(translate=True)
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

    work_version_ids = fields.One2many(comodel_name="music.work.version", inverse_name="work_id")
    version_qty = fields.Integer(compute="_compute_version_qty")

    @api.depends('title', 'composer_id')
    def _compute_name(self):
        for rec in self:
            rec.name = "%s: %s" % (rec.composer_id.name, rec.title)

    @api.depends('work_version_ids')
    def _compute_version_qty(self):
        for work in self:
            work.version_qty = len(work.work_version_ids)

    def action_open_versions_list(self):
        self.ensure_one()
        return {
            "name": _("All versions for %s" % self.name),
            "type": 'ir.actions.act_window',
            "res_model": 'music.work.version',
            "views": [[False, "tree"], [False, "form"]],
            "target": 'current',
            "domain": [('work_id', '=', self.id)],
            "context": {
                **self.env.context,
                'search_default_filter_group_by_composer_id': 0,
            },
        }

    def action_open_version_form(self):
        self.ensure_one()
        return {
            "name": _("Version for %s" % self.name),
            "type": 'ir.actions.act_window',
            "res_model": 'music.work.version',
            'res_id': self.work_version_ids[:1].id,
            "views": [[False, "form"]],
            "target": 'current',
            "context": {
                **self.env.context,
            },
        }

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

    def action_create_version(self):
        return {
            "name": _("Create version"),
            "type": 'ir.actions.act_window',
            "res_model": 'create.work.version.wizard',
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
            for mode in ['major', 'minor']:
                search_string = " in %s %s" % (note_string, mode[:3])
                works = self.env['music.work'].search([('tonality_note', '=', False), ('title', 'ilike', search_string)])
                works.write({'tonality_note': note.id, 'tonality_mode': mode})


