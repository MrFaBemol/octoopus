# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError



class Composer(models.Model):
    _name = "composer"
    _description = "A music composer"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    oo_id = fields.Integer(default=-1, tracking=True, string="OO ID")

    name = fields.Char(required=True, tracking=True)
    first_name = fields.Char()
    full_name = fields.Char(compute='_compute_names')
    display_name = fields.Char(compute='_compute_names')

    birth = fields.Date(required=True, tracking=True)
    death = fields.Date(tracking=True)

    portrait_url = fields.Char(tracking=True)
    biography = fields.Text()
    biography_short = fields.Text(compute="_compute_biography_short")
    
    country_ids = fields.Many2many(comodel_name="res.country")
    period_ids = fields.Many2many(comodel_name="period")

    is_popular = fields.Boolean(default=False)
    is_essential = fields.Boolean(default=False)

    slug_url = fields.Char()
    wikipedia_url = fields.Char()

    def name_get(self):
        res = []
        for composer in self:
            res.append((composer.id, composer.full_name))
        return res

    @api.depends('first_name', 'name', 'birth', 'death')
    def _compute_names(self):
        for rec in self:
            full_name = rec.name
            if rec.first_name:
                full_name += ", %s" % rec.first_name
            rec.full_name = full_name
            rec.display_name = "%s (%s - %s)" % (full_name, rec.birth.year, rec.death.year if rec.death else "")
            
    @api.depends('biography')
    def _compute_biography_short(self):
        for rec in self:
            rec.biography_short = rec.biography[:500] + " [...]" if rec.biography else ""


    def action_ask_open_opus(self):
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
        print("=====================================================")
        print(valid_composers)
        print(len(valid_composers))
        print("=====================================================")

        # wizard = self.env['oo.get.works.wizard'].create({'composer_ids': valid_composers.ids})

        # wizard.get_new_composers()
        # for composer in self:
        #     pass

