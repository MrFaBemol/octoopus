from odoo import api, fields, models, _
from unidecode import unidecode


class MusicComposer(models.Model):
    _name = "music.composer"
    _description = "A music composer"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin', 'website.seo.mixin']

    active = fields.Boolean(default=True)

    name = fields.Char(required=True, tracking=True)
    first_name = fields.Char(tracking=True)
    full_name = fields.Char(compute='_compute_names', store=True)
    display_name = fields.Char(compute='_compute_names', store=True)
    search_name = fields.Char(compute='_compute_names', store=True)
    birth = fields.Date(required=True, tracking=True)
    death = fields.Date(tracking=True)
    display_date = fields.Char(compute="_compute_display_date")

    portrait_url = fields.Char(tracking=True)
    biography = fields.Text(translate=True, default="")
    biography_short = fields.Text(compute="_compute_biography_short")
    country_ids = fields.Many2many(comodel_name="res.country")
    period_id = fields.Many2one(comodel_name="music.period", string="Period")
    is_popular = fields.Boolean(default=False)
    is_essential = fields.Boolean(default=False)

    work_ids = fields.One2many(comodel_name="music.work", inverse_name="composer_id")
    work_qty = fields.Integer(compute="_compute_work_qty")


    # Web
    wikipedia_url = fields.Char()



    def name_get(self):
        res = []
        for composer in self:
            res.append((composer.id, composer.full_name))
        return res


    # --------------------------------------------
    #                   COMPUTE
    # --------------------------------------------


    @api.depends('first_name', 'name', 'birth', 'death')
    def _compute_names(self):
        for composer in self:
            full_name = composer.name or ""
            if composer.first_name:
                full_name += ", %s" % composer.first_name
            composer.full_name = full_name
            composer.search_name = unidecode(full_name)
            composer.display_name = "%s (%s - %s)" % (full_name, composer.birth.year if composer.birth else "", composer.death.year if composer.death else "")

    @api.depends('birth', 'death')
    def _compute_display_date(self):
        for composer in self:
            composer.display_date = "%s - %s" % (composer.birth.year, composer.death.year)
            
    @api.depends('biography')
    def _compute_biography_short(self):
        for composer in self:
            composer.biography_short = composer.biography[:500] + " [...]" if composer.biography else ""

    @api.depends('work_ids')
    def _compute_work_qty(self):
        for composer in self:
            composer.work_qty = len(composer.work_ids)


    # --------------------------------------------
    #                   ACTIONS
    # --------------------------------------------


    def action_auto_fill_period(self):
        for composer in self:
            midlife_year = composer.birth.year + (composer.death.year - composer.birth.year)//2
            composer.period_id = self.env['music.period'].search([('date_start', '<=', '01-01-%s' % midlife_year), ('date_end', '>', '01-01-%s' % midlife_year)], limit=1)

    def action_show_works(self):
        self.ensure_one()
        return {
            "name": _("Works for %s" % self.full_name),
            "type": 'ir.actions.act_window',
            "res_model": 'music.work',
            "domain": [('id', 'in', self.work_ids.ids)],
            "views": [[False, "tree"], [False, "form"]],
        }






