# -*- coding: utf-8 -*-
from ..common.tools.oo_api import grant_access, call
import base64

import requests
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

# Todo: Add an action to update values with OpenOpus API + Get popular/essential composers

class Composer(models.Model):
    _name = "composer"
    _description = "A music composer"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True)
        
    oo_id = fields.Integer(default=-1, tracking=True, string="OO ID")
    name = fields.Char(required=True, tracking=True)
    first_name = fields.Char()
    full_name = fields.Char(compute='_compute_names')
    display_name = fields.Char(compute='_compute_names')
    birth = fields.Date(required=True, tracking=True)
    death = fields.Date(tracking=True)

    portrait = fields.Binary()
    portrait_url = fields.Char(tracking=True)
    biography = fields.Text(translate=True)
    biography_short = fields.Text(compute="_compute_biography_short")
    country_ids = fields.Many2many(comodel_name="res.country")
    period_ids = fields.Many2many(comodel_name="period", string="Periods")
    is_popular = fields.Boolean(default=False)
    is_essential = fields.Boolean(default=False)

    work_ids = fields.One2many(comodel_name="music.work", inverse_name="composer_id")
    work_count = fields.Integer(compute="_compute_work_count")

    oo_infos_url = fields.Char(compute="_compute_oo_infos_url")
    oo_works_url = fields.Char(compute="_compute_oo_works_url")
    slug_url = fields.Char()
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
            full_name = composer.name
            if composer.first_name:
                full_name += ", %s" % composer.first_name
            composer.full_name = full_name
            composer.display_name = "%s (%s - %s)" % (full_name, composer.birth.year if composer.birth else "", composer.death.year if composer.death else "")
            
    @api.depends('biography')
    def _compute_biography_short(self):
        for composer in self:
            composer.biography_short = composer.biography[:500] + " [...]" if composer.biography else ""

    @api.depends('work_ids')
    def _compute_work_count(self):
        for composer in self:
            composer.work_count = len(composer.work_ids)

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



    # --------------------------------------------
    #                   ACTIONS
    # --------------------------------------------

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
        res = call(self, 'composer/34', post)
        print("=====================================================")
        print(res)
        print("=====================================================")

