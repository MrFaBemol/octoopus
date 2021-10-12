# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class OOGetWorks(models.TransientModel):
    _name = "oo.get.works.wizard"
    _description = "A wizard to import works from OpenOpus API"

    composer_ids = fields.Many2many(comodel_name="composer")
    
    def get_new_works(self):
        api_url = self.env['ir.config_parameter'].sudo().get_param('open.opus.api')
        api_url += self.env['ir.config_parameter'].sudo().get_param('oo.api.all.works.by.composer.id')

        for composer in self.composer_ids:
            pass

        # for letter in ascii_lowercase:
        #     get_url = api_url + letter + ".json"
        #     response = requests.get(get_url)
        #     if response.status_code == 200 and response.text:
        #         response = response.json()
        #         if response['status']['success'] == 'true':
        #             for composer in response['composers']:
        #                 if not self.env['composer'].search([('oo_id', '=', composer['id'])]):
        #                     self.env['open.opus.new.composer'].create({
        #                         'wizard_id': self.id,
        #                         'oo_id': composer['id'],
        #                         'full_name': composer['complete_name'],
        #                         'name': composer['name'],
        #                         'birth': composer['birth'],
        #                         'death': composer['death'],
        #                         'portrait_url': composer['portrait'],
        #                     })



class OpenOpusNewMusicWork(models.TransientModel):
    _name = "oo.new.music.work"
    _description = "A work suggestion"

    composer_id = fields.Many2one(comodel_name="composer")
    title = fields.Char()
    
    
