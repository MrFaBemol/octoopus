from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import requests
import base64
import logging
_logger = logging.getLogger(__name__)



class MusicComposer(models.Model):
    _inherit = "music.composer"

    oo_id = fields.Integer(default=-1, tracking=True, string="OpenOpus ID")
    oo_infos_url = fields.Char(compute="_compute_oo_infos_url")
    oo_works_url = fields.Char(compute="_compute_oo_works_url")

    @api.depends('oo_id')
    def _compute_oo_infos_url(self):
        open_opus_api = self.env['ir.config_parameter'].sudo().get_param('open.opus.api')
        open_opus_composer_by_id = self.env['ir.config_parameter'].sudo().get_param('oo.api.composer.by.id')
        for composer in self:
            composer.oo_infos_url = "%s%s" % (
                open_opus_api,
                open_opus_composer_by_id.replace("{{ID}}", str(composer.oo_id)),
            )

    @api.depends('oo_id')
    def _compute_oo_works_url(self):
        open_opus_api = self.env['ir.config_parameter'].sudo().get_param('open.opus.api')
        open_opus_works_by_composer = self.env['ir.config_parameter'].sudo().get_param('oo.api.all.works.by.composer.id')
        for composer in self:
            composer.oo_works_url = "%s%s" % (
                open_opus_api,
                open_opus_works_by_composer.replace("{{ID}}", str(composer.oo_id)),
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
        valid_composers = self.env['music.composer'].search([('id', 'in', self.ids), ('oo_id', '!=', -1)])
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
                    composer.write({'image_1920': img})

