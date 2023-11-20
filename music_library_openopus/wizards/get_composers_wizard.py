
from datetime import datetime
from odoo import api, fields, models, _
from string import ascii_lowercase
import requests


class OOGetComposers(models.TransientModel):
    _name = "oo.get.composers.wizard"
    _description = "A wizard to import composers from OpenOpus API"

    composer_ids = fields.One2many("oo.new.composer", "wizard_id")

    def get_new_composers(self):
        api_url = self.env['ir.config_parameter'].sudo().get_param('open.opus.api')
        api_url += self.env['ir.config_parameter'].sudo().get_param('oo.api.composer.first.letter')

        for letter in ascii_lowercase:
            get_url = api_url.replace("{{ID}}", letter)
            response = requests.get(get_url)
            if response.status_code == 200 and response.text:
                response = response.json()
                if response['status']['success'] == 'true':
                    for composer in response['composers']:
                        if not self.env['music.composer'].search([('oo_id', '=', composer['id'])]):
                            # Todo: search on name of existing composer to make matches
                            existing_composer = self.env['music.composer'].search([('full_name', 'ilike', composer['complete_name'])], limit=1)
                            self.env['oo.new.composer'].create({
                                'wizard_id': self.id,
                                'oo_id': composer['id'],
                                'existing_composer_id': existing_composer.id,
                                'full_name': composer['complete_name'],
                                'name': composer['name'],
                                'birth': composer['birth'],
                                'death': composer['death'],
                                'portrait_url': composer['portrait'],
                            })


    def save_and_reopen_wizard(self):
        return {
            "name": _("Get new composers"),
            "type": 'ir.actions.act_window',
            "res_model": 'oo.get.composers.wizard',
            'res_id': self.id,
            "views": [[False, "form"]],
            "target": 'new',
            "context": {
                **self.env.context,
            },
        }

    def action_import_composers(self):
        self.composer_ids.import_composer()



class OpenOpusNewComposer(models.TransientModel):
    _name = "oo.new.composer"
    _description = "A composer suggestion"

    wizard_id = fields.Many2one(comodel_name="oo.get.composers.wizard")
    oo_id = fields.Integer()
    existing_composer_id = fields.Many2one("music.composer")
    full_name = fields.Char()
    name = fields.Char()
    birth = fields.Char()
    death = fields.Char()
    portrait_url = fields.Char()

    def import_composer(self):
        vals_list = []

        for rec in self:
            birth = datetime.strptime(rec.birth, '%Y-%m-%d').date()
            death = datetime.strptime(rec.death, '%Y-%m-%d').date() if rec.death else False

            first_name = rec.full_name.replace(rec.name, "").strip()

            vals = {
                'oo_id': rec.oo_id,
                'name': rec.name,
                'first_name': first_name,
                'birth': birth,
                'death': death,
                'portrait_url': rec.portrait_url,
            }

            if rec.existing_composer_id:
                rec.existing_composer_id.write(vals)
            else:
                vals_list.append(vals)

        self.env['music.composer'].create(vals_list)
