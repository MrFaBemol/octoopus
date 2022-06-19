# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.addons.http_routing.models.ir_http import slug

from ..common.tools.oo_api import grant_access, call_api
import requests
import base64
from unidecode import unidecode


# Todo: Add an action to update values with OpenOpus API + Get popular/essential composers

class Composer(models.Model):
    _name = "composer"
    _description = "A music composer"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True)
        
    oo_id = fields.Integer(default=-1, tracking=True, string="OO ID")
    name = fields.Char(required=True, tracking=True)
    first_name = fields.Char(tracking=True)
    full_name = fields.Char(compute='_compute_names', store=True)
    display_name = fields.Char(compute='_compute_names', store=True)
    search_name = fields.Char(compute='_compute_names', store=True)
    birth = fields.Date(required=True, tracking=True)
    death = fields.Date(tracking=True)

    portrait = fields.Binary()
    portrait_url = fields.Char(tracking=True)
    biography = fields.Text(translate=True)
    biography_short = fields.Text(compute="_compute_biography_short")
    country_ids = fields.Many2many(comodel_name="res.country")
    period_ids = fields.Many2many(comodel_name="period", relation="composer_period_rel", string="Periods")
    is_popular = fields.Boolean(default=False)
    is_essential = fields.Boolean(default=False)

    work_ids = fields.One2many(comodel_name="music.work", inverse_name="composer_id")
    work_qty = fields.Integer(compute="_compute_work_qty")

    published = fields.Boolean(default=False)

    # Web
    oo_infos_url = fields.Char(compute="_compute_oo_infos_url")
    oo_works_url = fields.Char(compute="_compute_oo_works_url")
    slug_url = fields.Char(compute="_compute_slug_url")
    wikipedia_url = fields.Char()

    # IMSLP
    imslp_composer_id = fields.Many2one(comodel_name="imslp.composer", compute="_compute_imslp_composer_id", search="_search_imslp_composer")
    imslp_url = fields.Char(related="imslp_composer_id.url")
    imslp_works = fields.One2many(related="imslp_composer_id.imslp_work_ids")
    imslp_pending_works = fields.Many2many(comodel_name="imslp.work", compute="_compute_imslp_works_infos")
    imslp_pending_works_qty = fields.Integer(compute="_compute_imslp_works_infos")


    def name_get(self):
        res = []
        for composer in self:
            res.append((composer.id, composer.full_name))
        return res

    def _search_imslp_composer(self, operator, value):
        op = "not in" if not value and operator == "=" else "in"
        domain = [("name", "ilike", value)] if value else []
        return [('id', op, self.env['imslp.composer'].search(domain).composer_id.ids)]

    # --------------------------------------------
    #                   COMPUTE
    # --------------------------------------------

    @api.depends('first_name', 'name', 'birth', 'death')
    def _compute_names(self):
        for composer in self:
            full_name = composer.name
            if composer.first_name:
                full_name += ", %s" % composer.first_name
            composer.full_name = full_name
            composer.search_name = unidecode(full_name)
            composer.display_name = "%s (%s - %s)" % (full_name, composer.birth.year if composer.birth else "", composer.death.year if composer.death else "")
            
    @api.depends('biography')
    def _compute_biography_short(self):
        for composer in self:
            composer.biography_short = composer.biography[:500] + " [...]" if composer.biography else ""

    @api.depends('work_ids')
    def _compute_work_qty(self):
        for composer in self:
            composer.work_qty = len(composer.work_ids)

    @api.depends('oo_id')
    def _compute_oo_infos_url(self):
        for composer in self:
            composer.oo_infos_url = "%s%s" % (
                self.env['ir.config_parameter'].sudo().get_param('open.opus.api'),
                self.env['ir.config_parameter'].sudo().get_param('oo.api.composer.by.id').replace("{{ID}}", str(composer.oo_id)),
            )

    @api.depends('oo_id')
    def _compute_oo_works_url(self):
        for composer in self:
            composer.oo_works_url = "%s%s" % (
                self.env['ir.config_parameter'].sudo().get_param('open.opus.api'),
                self.env['ir.config_parameter'].sudo().get_param('oo.api.all.works.by.composer.id').replace("{{ID}}", str(composer.oo_id)),
            )

    @api.depends('name', 'first_name', 'birth', 'death')
    def _compute_slug_url(self):
        for composer in self:
            composer.slug_url = slug(composer) if composer.id else ""


    def _compute_imslp_composer_id(self):
        for composer in self:
            composer.imslp_composer_id = self.env['imslp.composer'].search([('composer_id', '=', composer.id)], limit=1)

    @api.depends('imslp_composer_id', 'work_ids')
    def _compute_imslp_works_infos(self):
        for composer in self:
            composer.imslp_pending_works = composer.imslp_works.filtered(lambda w: not w.work_id)
            composer.imslp_pending_works_qty = len(composer.imslp_pending_works)


    # --------------------------------------------
    #                   ACTIONS
    # --------------------------------------------


    def action_switch_published(self):
        for composer in self:
            composer.published = not composer.published

    def action_show_works(self):
        self.ensure_one()
        return {
            "name": _("Works for %s" % self.full_name),
            "type": 'ir.actions.act_window',
            "res_model": 'music.work',
            "domain": [('id', 'in', self.work_ids.ids)],
            "views": [[False, "tree"], [False, "form"]],
        }

    def action_show_imslp_pending_works(self):
        self.ensure_one()
        return {
            "name": _("Pending works for %s" % self.full_name),
            "type": 'ir.actions.act_window',
            "res_model": 'imslp.work',
            "domain": [('id', 'in', self.imslp_works.ids)],
            "views": [[False, "tree"]],
            "context": {
                **self.env.context,
                'search_default_filter_pending': 1,
            }
        }


    def action_oo_get_composers(self):
        wizard = self.env['oo.get.composers.wizard'].create({})
        wizard.get_new_composers()

        return {
            "name": _("Get new composers"),
            "type": 'ir.actions.act_window',
            "res_model": 'oo.get.composers.wizard',
            'res_id': wizard.id,
            "views": [[False, "form"]],
            "target": 'new',
            "context": {
                **self.env.context,
            },
        }

    def action_oo_get_works(self):
        valid_composers = self.env['composer'].search([('id', 'in', self.ids), ('oo_id', '!=', -1)])
        wizard = self.env['oo.get.works.wizard'].create({'composer_ids': valid_composers.ids})
        wizard.get_new_works()
        return {
            "name": _("Get new works"),
            "type": 'ir.actions.act_window',
            "res_model": 'oo.get.works.wizard',
            'res_id': wizard.id,
            "views": [[False, "form"]],
            "target": 'new',
            "context": {
                **self.env.context,
            },
        }

    def action_oo_get_portrait(self):
        for composer in self:
            if composer.portrait_url:
                response = requests.get(composer.portrait_url, verify=False)
                if response.status_code == 200:
                    img = base64.b64encode(response.content)
                    composer.write({'portrait': img})



    # --------------------------------------------
    #                   API
    # --------------------------------------------


    @grant_access
    def action_api_test(self):
        post = {
            'fields': ['name', 'first_name', 'portrait_url'],
        }
        res = call_api(self, 'composer/34', post)
        # print(res)

        # response = urlopen(self.env['composer'].browse(15).imslp_url)
        # html = response.read().decode("utf-8")
        # soup = BeautifulSoup(html, "html.parser")
        #
        # header = soup.find_all("div", attrs={'class': "cp_firsth"})
        # header[0].script.extract()
        # header[0].h2.extract()
        # if header[0].span:
        #     header[0].span.extract()
        # date_str = header[0].text.replace("\n", "").replace("(", "").replace(")", "").split(" — ")
        #
        # dates = [datetime.datetime.strptime(d, "%d %B %Y") for d in date_str]
        # print("=====================================================")
        # print(dates)
        # print("=====================================================")

