from odoo import api, fields, models, _


class MusicWork(models.Model):
    _name = 'music.work'
    _description = "A music work that may have multiple versions"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'website.seo.mixin']
    _order = 'title'
    
    active = fields.Boolean(default=True)
    """
        to_check is mainly used for automatic creation, when infos might not be consistent.
        Ex: if two instruments are found when creating a version (ex clarinet in A/B-flat), choose the default (or a random one) and flag the record
    """
    to_check = fields.Boolean(default=False)
    to_check_reason = fields.Char()

    composer_id = fields.Many2one(comodel_name="music.composer", required=True, ondelete='restrict')
    composer_portrait = fields.Image(related="composer_id.avatar_1920")
    title = fields.Char(required=True, translate=True)
    sub_title = fields.Char(translate=True)
    nickname = fields.Char(translate=True)
    name = fields.Char(compute="_compute_name")

    catalogue = fields.Char()
    catalogue_number = fields.Integer(default=False)
    catalogue_piece_number = fields.Integer(default=False)

    # Stored as a string because it's more convenient. Sometimes we have to write "1849-1852" because composer was lazy
    date_composition = fields.Char(string="Composition date")
    date_first_publication = fields.Char(string="First publication date")
    period_id = fields.Many2one(comodel_name="music.period")
    duration = fields.Char()
    dedication = fields.Char()

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


    # --------------------------------------------
    #                   COMPUTE
    # --------------------------------------------


    @api.depends('title', 'composer_id')
    def _compute_name(self):
        for rec in self:
            rec.name = "%s: %s" % (rec.composer_id.name, rec.title)

    @api.depends('work_version_ids')
    def _compute_version_qty(self):
        for work in self:
            work.version_qty = len(work.work_version_ids)


    # --- WEB / SEO ---


    @api.depends('title', 'catalogue', 'sub_title', 'nickname', 'composer_id.full_name')
    def _compute_seo_name(self):
        for work in self:
            name = work.title
            if work.catalogue:
                name += " %s" % work.catalogue
            if work.sub_title:
                name += " - %s" % work.sub_title
            if work.nickname:
                name += " (%s)" % work.nickname

            work.seo_name = "%s - %s" % (work.composer_id.full_name, name) if work.id else ""

    # TODO: ajouter une action pour voir les infos d'imslp depuis la vue de ce modèle

    # --------------------------------------------
    #                MISC METHODS
    # --------------------------------------------


    def search_by_key(self, key=None):
        return self.env['music.work.version'].search_by_key(key)

    def _create_version(self, instrumentation, is_original=False):
        if not instrumentation:
            return

        for work in self:
            new_version = self.env['music.work.version'].create({'work_id': work.id, 'is_original': is_original})
            vals_list = [{
                'work_version_id': new_version.id,
                'instrument_id': instrument.id if instrument._name == 'music.instrument' else False,
                'quantity': qty,
            } for instrument, qty in instrumentation.items()]
            self.env['music.work.version.instrument'].create(vals_list)


    # --------------------------------------------
    #                   STANDARD
    # --------------------------------------------


    @api.model_create_multi
    def create(self, vals_list):
        instrumentation_list = [vals.pop('instrumentation', None) for vals in vals_list]
        res = super(MusicWork, self).create(vals_list)

        # Create music.work.version if instrumentation was passed in vals
        for work, instrumentation in zip(res, instrumentation_list):
            work._create_version(instrumentation, is_original=True)

        return res


    def write(self, vals):
        if 'active' in vals:
            self.work_version_ids.write({'active': vals.get('active')})
        return super(MusicWork, self).write(vals)


    # --------------------------------------------
    #                   ACTIONS
    # --------------------------------------------


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

    # Todo: check if I keep it as is
    def action_auto_fill_tonality(self):
        for note in self.env['music.note'].search([]):
            note_string = "%s%s" % (note.note, " "+note.alt if note.alt else "")
            for mode in ['major', 'minor']:
                search_string = " in %s %s" % (note_string, mode[:3])
                works = self.env['music.work'].search([('tonality_note', '=', False), ('title', 'ilike', search_string)])
                works.write({'tonality_note': note.id, 'tonality_mode': mode})


