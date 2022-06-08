# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import time
import requests
import logging
_logger = logging.getLogger(__name__)

class ImslpWork(models.Model):
    _name = "imslp.work"
    _description = "A line with name + link to an imslp work (+m2o to imslp composer)"

    name = fields.Char(required=True, readonly=True)
    url = fields.Char(required=True, readonly=True)
    composer_name = fields.Char(required=True, readonly=True)

    work_id = fields.Many2one(comodel_name="music.work")
    imslp_composer_id = fields.Many2one(comodel_name="imslp.composer")
    composer_id = fields.Many2one(related="imslp_composer_id.composer_id")

    def action_open_url(self):
        self.ensure_one()
        if self.url:
            return {
                'type': 'ir.actions.act_url',
                'target': 'new',
                'url': self.url,
            }

    @api.model
    def create(self, vals):
        if existing_composer := self.env['imslp.composer'].search([('name', '=', vals.get("composer_name", ""))]):
            vals.update({'imslp_composer_id': existing_composer.id})
        if existing_work := self.env['music.work'].search([('title', '=', vals.get("composer_name", ""))]):
            vals.update({'work_id': existing_work.id})
        return super(ImslpWork, self).create(vals)


    def _cron_fetch_imslp_works(self):
        url = self.env['ir.config_parameter'].sudo().get_param('imslp.api').replace("{{TYPE}}", "2")
        first_request_start = start = int(self.env['ir.config_parameter'].sudo().get_param('imslp.work.start'))

        clock = time.perf_counter()
        while time.perf_counter() - clock < 840:
            try:
                _logger.info("Calling IMSLP api : %s" % url.replace("{{START}}", str(start)))
                response = requests.get(url.replace("{{START}}", str(start)))
                if response.status_code == 200 and response.text:
                    response = response.json()
                    metadata = response.pop("metadata")

                    existing_works_urls = self.env['imslp.work'].search([("url", "in", [w.get('permlink') for w in response.values()])]).mapped('url')
                    vals = [{
                        "name": work.get('intvals').get('worktitle'),
                        "url": work.get('permlink'),
                        "composer_name": work.get('intvals').get('composer'),
                    } for work in response.values() if work.get('permlink') not in existing_works_urls]


                    if metadata.get('moreresultsavailable'):
                        start += metadata.get('limit')
                    else:
                        start = 0

                    res = self.sudo().create(vals)
                    self.env['ir.config_parameter'].sudo().set_param("imslp.work.start", str(start))
                    self.env.cr.commit()

                    if res:
                        _logger.info("%s records created!" % len(res))
                    if start == first_request_start:
                        break

            except Exception as e:
                self.env.cr.rollback()
                _logger.error("Error on cron _cron_fetch_imslp_works : Exception: %s" % e)

