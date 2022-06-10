# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from dateutil import relativedelta

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from ..common.tools.misc import iri2uri
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

    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('parsed', 'Parsed'),
            ('error', 'Parsing error'),
            ('deleted', 'Deleted'),
        ],
        default='new',
        required=True,
    )
    next_update = fields.Datetime()
    infos_ids = fields.One2many(comodel_name="imslp.work.infos", inverse_name="work_id")

    # --------------------------------------------
    #                   ACTIONS
    # --------------------------------------------
    def action_open_url(self):
        self.ensure_one()
        if self.url:
            return {
                'type': 'ir.actions.act_url',
                'target': 'new',
                'url': self.url,
            }

    def action_view_imslp_infos(self):
        self.ensure_one()
        if self.infos_ids:
            return {
                "name": _("Imslp infos for %s", self.name),
                "type": 'ir.actions.act_window',
                "res_model": 'imslp.work.infos',
                "views": [[False, "tree"]],
                "target": 'new',
                "domain": [('id', 'in', self.infos_ids.ids)],
            }

    def action_get_webpage_infos(self):
        for composer in self:
            composer._get_webpage_infos()

    # --------------------------------------------
    #                   PARSING
    # --------------------------------------------
    def _log_exception(self, msg, level='error', state='error'):
        """
        Easy log system with state change
            :param msg: The message to be displayed in logger
            :param level: error / warning / info
            :param state: record will get this state
        """
        getattr(_logger, level)(msg)
        self.state = state


    def _get_webpage_infos(self):
        self.ensure_one()
        self.state = 'parsed'
        # The key/value pairs
        vals = {}
        try:
            response = urlopen(iri2uri(self.url))
            html = response.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")

            # Sub-methods are called to get infos
            vals.update(self._parse_general_infos(soup))

        except HTTPError as e:
            if e.code == 404:
                self._log_exception("IMSLP page for %s has been deleted (%s)" % (self.name, self.url), level="warning", state='deleted')
        except UnicodeEncodeError as e:
            self._log_exception("Unicode Error for %s: %s" % (self.name, e))
        except Exception as e:
            self._log_exception("[%s] Error for %s: %s" % (type(e).__name__, self.name, e))

        # Create/Update all key/value pairs
        for key, value in vals.items():
            if existing_log := self.env['imslp.work.infos'].search([('work_id', '=', self.id), ('key', '=', key)]):
                existing_log.value = value
            else:
                self.env['imslp.work.infos'].create([{'work_id': self.id, 'key': key, 'value': value}])

        # Log update
        self.next_update = fields.Datetime.now() + relativedelta.relativedelta(days=7)


    def _parse_general_infos(self, soup):
        res = {}
        header = soup.find_all("div", attrs={'class': "wi_body"})
        if not header or len(header) > 1:
            raise ValueError("Page should have exactly one div with class `wi_body`")

        # We don't want lines that are not displayed
        lines = filter(lambda l: 'udelonly' not in l.get('class', []), header[0].find_all("tr"))

        for line in lines:
            for tag in ["th", "td"]:
                if node := line.find(tag).find("span", attrs={'class': "ms555"}):
                    node.decompose()
            res.update({line.find("th").text.strip(): line.find("td").text.strip()})
        return res



    # --------------------------------------------
    #                   STANDARD
    # --------------------------------------------


    @api.model
    def create(self, vals):
        if existing_composer := self.env['imslp.composer'].search([('name', '=', vals.get("composer_name", ""))]):
            vals.update({'imslp_composer_id': existing_composer.id})
            if existing_work := self.env['music.work'].search([('composer_id', '=', existing_composer.id), ('title', '=', vals.get("name", ""))]):
                vals.update({'work_id': existing_work.id})
        return super(ImslpWork, self).create(vals)

    # --------------------------------------------
    #                   CRON
    # --------------------------------------------

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

