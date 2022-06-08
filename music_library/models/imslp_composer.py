# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

import requests
import time
import logging
_logger = logging.getLogger(__name__)

class ImslpComposer(models.Model):
    _name = "imslp.composer"
    _description = "A line with name + link to an imslp composer"

    name = fields.Char(required=True, readonly=True)
    url = fields.Char(required=True, readonly=True)
    composer_id = fields.Many2one(comodel_name="composer")
    imslp_work_ids = fields.One2many(comodel_name="imslp.work", inverse_name="imslp_composer_id")
    imslp_work_qty = fields.Integer(compute="_compute_imslp_work_qty", store=True)

    @api.depends('imslp_work_ids')
    def _compute_imslp_work_qty(self):
        for composer in self:
            composer.imslp_work_qty = len(composer.imslp_work_ids)

    def action_open_url(self):
        self.ensure_one()
        if self.url:
            return {
                'type': 'ir.actions.act_url',
                'target': 'new',
                'url': self.url,
            }

    def action_view_imslp_works(self):
        self.ensure_one()
        if self.imslp_work_ids:
            return {
                "name": _("Imslp works for %s", self.name),
                "type": 'ir.actions.act_window',
                "res_model": 'imslp.work',
                "views": [[False, "tree"]],
                "target": 'new',
                "domain": [('id', 'in', self.imslp_work_ids.ids)],
                "context": {
                    **self.env.context,
                },
            }


    @api.model
    def create(self, vals):
        name = vals.get('name').split(", ")
        if len(name) > 1:
            if existing_composer := self.env['composer'].search([('name', 'ilike', name[0]), ('first_name', 'ilike', name[1])], limit=1):
                vals.update({'composer_id': existing_composer.id})
        return super(ImslpComposer, self).create(vals)


    def _cron_fetch_imslp_composers(self):
        url = self.env['ir.config_parameter'].sudo().get_param('imslp.api').replace("{{TYPE}}", "1")
        first_request_start = start = int(self.env['ir.config_parameter'].sudo().get_param('imslp.composer.start'))

        clock = time.perf_counter()
        while time.perf_counter() - clock < 840:
            try:
                _logger.info("Calling IMSLP api : %s" % url.replace("{{START}}", str(start)))
                response = requests.get(url.replace("{{START}}", str(start)))
                if response.status_code == 200 and response.text:
                    response = response.json()
                    metadata = response.pop("metadata")

                    existing_composers_urls = self.env['imslp.composer'].search([("url", "in", [c.get('permlink') for c in response.values()])]).mapped('url')
                    vals = [{
                        "name": composer.get('id').replace("Category:", ""),
                        "url": composer.get('permlink')
                    } for composer in response.values() if composer.get('permlink') not in existing_composers_urls]


                    if metadata.get('moreresultsavailable'):
                        start += metadata.get('limit')
                    else:
                        start = 0

                    res = self.sudo().create(vals)
                    self.env['ir.config_parameter'].sudo().set_param("imslp.composer.start", str(start))
                    self.env.cr.commit()

                    if res:
                        _logger.info("%s records created!" % len(res))
                    if start == first_request_start:
                        break

            except Exception as e:
                self.env.cr.rollback()
                _logger.error("Error on cron _cron_fetch_imslp_composers : Exception: %s" % e)

