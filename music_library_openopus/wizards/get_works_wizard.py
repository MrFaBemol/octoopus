
import requests
from odoo import api, fields, models, _


class OOGetWorks(models.TransientModel):
    _name = "oo.get.works.wizard"
    _description = "A wizard to import works from OpenOpus API"

    composer_ids = fields.Many2many("composer")
    work_ids = fields.One2many("oo.new.work", "wizard_id")
    works_count = fields.Integer(compute="_compute_work_count")

    @api.depends('work_ids')
    def _compute_work_count(self):
        for rec in self:
            rec.works_count = len(rec.work_ids)
    
    def get_new_works(self):
        api_url = self.env['ir.config_parameter'].sudo().get_param('open.opus.api')
        api_url += self.env['ir.config_parameter'].sudo().get_param('oo.api.all.works.by.composer.id')

        for composer in self.composer_ids:
            get_url = api_url.replace("{{ID}}", str(composer.oo_id))
            response = requests.get(get_url)

            if response.status_code == 200 and response.text:
                response = response.json()

                if response['status']['success'] == 'true':
                    for work in response['works']:
                        if not self.env['music.work'].search([('oo_id', '=', work['id'])]):
                            self.env['oo.new.work'].create({
                                'wizard_id': self.id,
                                'oo_id': work['id'],
                                'oo_genre': work['genre'],
                                'composer_id': composer.id,
                                'title': work['title'],
                                'sub_title': work['subtitle'],
                                'is_popular': work['popular'] == "1",
                                'is_essential': work['recommended'] == "1",
                            })

    def action_import_works(self):
        self.work_ids.import_work()


class OpenOpusNewWork(models.TransientModel):
    _name = "oo.new.work"
    _description = "A work suggestion"

    wizard_id = fields.Many2one(comodel_name="oo.get.works.wizard")
    oo_id = fields.Integer(default=-1)
    oo_genre = fields.Char()

    composer_id = fields.Many2one(comodel_name="music.composer")
    title = fields.Char()
    sub_title = fields.Char()

    is_popular = fields.Boolean(default=False)
    is_essential = fields.Boolean(default=False)

    def import_work(self):
        for rec in self:
            self.env['music.work'].create({
                'composer_id': rec.composer_id.id,
                'oo_id': rec.oo_id,
                'oo_genre': rec.oo_genre,
                'title': rec.title,
                'sub_title': rec.sub_title,
                'is_popular': rec.is_popular,
                'is_essential': rec.is_essential,
            })



    
