
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from odoo.addons.music_library.utils.misc import iri2uri
import requests
import time
import logging
import datetime
import re

_logger = logging.getLogger(__name__)


class ImslpComposer(models.Model):
    _name = "imslp.composer"
    _description = "Imslp composer"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, readonly=True)
    url = fields.Char(required=True, readonly=True)
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
    composer_id = fields.Many2one(comodel_name="music.composer", tracking=True)
    imslp_work_ids = fields.One2many(comodel_name="imslp.work", inverse_name="imslp_composer_id")
    imslp_work_qty = fields.Integer(compute="_compute_imslp_work_qty", store=True)
    infos_ids = fields.One2many(comodel_name="imslp.composer.infos", inverse_name="composer_id")

    @api.depends('imslp_work_ids')
    def _compute_imslp_work_qty(self):
        for composer in self:
            composer.imslp_work_qty = len(composer.imslp_work_ids)

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

    def action_view_imslp_infos(self):
        self.ensure_one()
        if self.infos_ids:
            return {
                "name": _("Imslp infos for %s", self.name),
                "type": 'ir.actions.act_window',
                "res_model": 'imslp.composer.infos',
                "views": [[False, "tree"]],
                "target": 'new',
                "domain": [('id', 'in', self.infos_ids.ids)],
            }


    def action_link_composer(self):
        for composer in self:
            name_split = composer.name.split(", ")
            if len(name_split) > 1 and (existing_composer := self.env['music.composer'].search([('name', 'ilike', name_split[0]), ('first_name', 'ilike', name_split[1])], limit=1)):
                composer.composer_id = existing_composer

    def action_get_webpage_infos(self):
        for composer in self:
            composer._get_webpage_infos()


    def action_create_update_composer(self):
        parsed_composers = self.filtered(lambda c: c.state == 'parsed')
        _logger.info(_("Creating/Updating %s (/%s) composers", len(parsed_composers), len(self)))

        for composer in parsed_composers:
            composer._create_update_composer()


    # --------------------------------------------
    #            CREATE/UPDATE COMPOSER
    # --------------------------------------------


    def _create_update_composer(self):
        """ Get data from imslp.composer.infos and create a composer or update the linked one """
        try:
            self.ensure_one()
            _logger.info("Creating new composer from imslp (%s)" % self.name)

            vals = {
                'imslp_composer_id': self.id,
                **self._get_dates(),
                # Todo: add name
                # Todo: add portrait
            }

            if not self.composer_id:
                new_music_composer = self.env['music.composer'].create(vals)
                self.write({'composer_id': new_music_composer.id})
            else:
                self.composer_id.write(vals)
            return self.composer_id

        except Exception as e:
            self._log_exception("[%s] Create/update error for %s: %s" % (type(e).__name__, self.name, e))
            raise e


    def _get_dates(self):
        vals = {}
        date_re = r"\d{1,2} [A-Za-z]* \d{4}"
        birth = self.get_info("birth")
        death = self.get_info("death")
        if res := re.match(date_re, birth):
            vals.update({'birth': datetime.datetime.strptime(res.group(), "%d %B %Y")})
        if res := re.match(date_re, death):
            vals.update({'death': datetime.datetime.strptime(res.group(), "%d %B %Y")})
        return vals



    # --------------------------------------------
    #                   MISC
    # --------------------------------------------


    def _log_exception(self, msg: str, level: str = 'error', state: str = 'error'):
        """
        Easy log system with state change
            :param msg: The message to be displayed in logger
            :param level: error / warning / info
            :param state: record will get this state
        """
        getattr(_logger, level)(msg)
        self.state = state

    def get_info(self, key):
        return self.infos_ids.filtered(lambda i: i.key == key).value or ""

    # --------------------------------------------
    #                   PARSING
    # --------------------------------------------


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
            vals.update(self._parse_dates(soup))
            vals.update(self._parse_portrait(soup))

        except HTTPError as e:
            if e.code == 404:
                self._log_exception("IMSLP page for %s has been deleted (%s)" % (self.name, self.url), level="warning", state='deleted')
        except UnicodeEncodeError as e:
            self._log_exception("Unicode Error for %s: %s" % (self.name, e))
        except Exception as e:
            self._log_exception("[%s] Error for %s: %s" % (type(e).__name__, self.name, e))

        # Create/Update all key/value pairs
        for key, value in vals.items():
            if existing_log := self.env['imslp.composer.infos'].search([('composer_id', '=', self.id), ('key', '=', key)]):
                existing_log.value = value
            else:
                self.env['imslp.composer.infos'].create([{'composer_id': self.id, 'key': key, 'value': value}])

        # Log update
        self.next_update = fields.Datetime.now() + relativedelta.relativedelta(days=7)

    def _parse_portrait(self, soup):
        res = {}
        try:
            portrait = soup.find("div", attrs={'class': "cp_img"}).find("div", attrs={'class': "floatnone"}).find("img")
            if portrait_url := portrait.get('src', ""):
                res['portrait_url'] = "https://imslp.org%s" % portrait_url
        except Exception as e:
            self._log_exception("Wrong parsing of url portrait for %s" % self.name)
        return res

    def _parse_dates(self, soup):
        res = {}
        header = soup.find("div", attrs={'class': "cp_firsth"})
        for a in ["script", "h2", "span"]:
            if node := getattr(header, a, None):
                node.extract()
        date_str = header.text
        for c in "\n()":
            date_str = date_str.replace(c, "")
        date_str = date_str.strip()
        try:
            # Todo: datetime.datetime.strptime(d, "%d %B %Y")
            # Todo: .replace("b.", "").replace("d.", "").strip()
            for key, val in zip(["birth", "death"], date_str.split(" — ")):
                res[key] = val
        except ValueError:
            self._log_exception("Wrong date format for %s : %s" % (self.name, date_str))
        return res


    # --------------------------------------------
    #                   CRUD
    # --------------------------------------------


    @api.model_create_multi
    def create(self, vals):
        """ When creating an imslp composer, we try to find an existing composer to link the 2 records """
        res = super(ImslpComposer, self).create(vals)
        res.action_link_composer()
        return res

    # --------------------------------------------
    #                   CRON
    # --------------------------------------------

    def _cron_fetch_imslp_composers(self):
        url = self.env['ir.config_parameter'].sudo().get_param('imslp.api').replace("{{TYPE}}", "1")
        first_request_start = start = int(self.env['ir.config_parameter'].sudo().get_param('imslp.composer.start'))

        clock = time.perf_counter()
        while time.perf_counter() - clock < 840:
            try:
                _logger.info("Calling IMSLP api composers : %s" % url.replace("{{START}}", str(start)))
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
