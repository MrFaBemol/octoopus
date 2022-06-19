# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from ..common.tools.misc import iri2uri
from collections import defaultdict
import time
import re
import math
import requests
import logging
_logger = logging.getLogger(__name__)

class ImslpWork(models.Model):
    _name = "imslp.work"
    _description = "A line with name + link to an imslp work (+m2o to imslp composer)"

    name = fields.Char(required=True, readonly=True)
    url = fields.Char(required=True, readonly=True)
    composer_name = fields.Char(required=True, readonly=True)

    work_id = fields.Many2one(comodel_name="music.work", domain="[('composer_id', '=', composer_id)]")
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

    def action_create_update_work(self):
        keys = set(self.infos_ids.mapped('key'))

        # Todo: GET ALL KEYS
        print("=====================================================")
        for key in keys:
            works = self.env['imslp.work.infos'].search([('key', '=', key)]).work_id.filtered(lambda w: w.id in self.ids)
            print("%s => %s" % (key, len(works)))
        print("=====================================================")

        # Todo: GET POSSIBLE VALUES BY KEY
        """
            [OK] "Opus/Catalogue Number"
            [OK] "Composer Time Period"              => Créer une nouvelle "period" si besoin
            [OK] "Year/Date of Composition"     => Tel quel dans date
            [OK] "Average Duration"             => Tel quel NOUVEAU CHAMP
            [OK] "Alternative Title"            => Tel quel dans sub_title
            [OK] "Dedication"                   => Virer les dates (XXXX-XXXX) NOUVEAU CHAMP
            [OK] "First Publication"            => Récup la date (premiers char jusqu'à l'espace) NOUVEAU CHAMP
            "Movements/Sections"                => NEW MODEL
        """
        key = "Name Aliases"
        res = self.env['imslp.work.infos'].search([('key', '=', key), ('work_id', 'in', self.ids)])
        print("=====================================================")
        # print("\n".join(set(res.mapped('value'))))
        # print("\n".join(["%s => %s" % (i.value, i.work_id.name) for i in res]))
        print("=====================================================")

        print("=====================================================")
        for work in self:
            work._create_update_work()
        print("=====================================================")





    # --------------------------------------------
    #               MISC METHODS
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

    def get_info(self, key):
        return self.infos_ids.filtered(lambda i: i.key == key).value or ""

    # --------------------------------------------
    #              CREATE/UPDATE WORK
    # --------------------------------------------

    def _create_update_work(self):
        try:
            self.ensure_one()
            if not self.composer_id:
                raise ValidationError("%s (%s) is not linked to an existing composer!" % (self.name, self.composer_name))
            _logger.info("Creating new work from imslp (%s - %s)" % (self.composer_name, self.name))

            vals = {'imslp_work_id': self.id}
            vals.update(self._get_tonality())
            vals.update(self._get_date_composition())
            vals.update(self._get_sub_title())
            vals.update(self._get_catalogue())
            vals.update(self._get_duration())
            vals.update(self._get_dedication())
            vals.update(self._get_date_first_publication())
            vals.update(self._get_composer_period())

            if not self.work_id:
                """
                    A few values are set at creation, and will never be modified with this action (eq. noupdate="1")
                    - Composer
                    - Title
                    - Original instrumentation
                """
                vals.update({'composer_id': self.composer_id.id, 'title': self.name})
                vals.update(self._get_instrumentation())
                self.write({'work_id': self.env['music.work'].create(vals).id})
            else:
                self.work_id.write(vals)

            # print("[%s]\n%s" % (self.work_id, vals))
            return self.work_id
        except Exception as e:
            self._log_exception("[%s] Create/update error for %s: %s" % (type(e).__name__, self.name, e))


    def _get_tonality(self):
        if res := re.search(r"[A-G](-(flat|sharp))? (minor|major)?", self.get_info("Key")):
            note, mode = res.group().lower().split(" ")
            domain = [('note', '=', note[0])]
            domain += [('alt', '=', note[2:])] if "-" in note else [('alt', '=', False)]
            note_id = self.env['music.note'].search(domain)
            return {'tonality_note': note_id.id, 'tonality_mode': mode}
        return {}

    def _get_date_composition(self):
        return {'date_composition': self.get_info("Year/Date of Composition") or False}

    def _get_sub_title(self):
        return {'sub_title': self.get_info("Alternative Title") or False}

    def _get_catalogue(self):
        return {'catalogue': self.get_info("Opus/Catalogue Number") or False}

    def _get_duration(self):
        return {'duration': self.get_info("Average Duration") or False}

    def _get_dedication(self):
        if res := self.get_info("Dedication"):
            res = re.sub(r"\(\d{4}-\d{4}\)", "", res.replace("\n", " ")).strip()
            return {'dedication': res}
        return {}

    def _get_date_first_publication(self):
        if res := re.match(r"^(\d{4}(-\d{2,4})?)", self.get_info("First Publication")):
            res = (res.groups())[0]
            return {'date_first_publication': res}
        return {}

    def _get_composer_period(self):
        if res := self.get_info("Composer Time Period"):
            return {'period_id': self.env['period'].search_or_create_by_name(res.strip()).id}
        return {}

    def _get_instrumentation(self):
        """
        Parse the webpage 'Instrumentation' line and try to understand which performers are needed for the original version
        :return: a dict{} with: key=instrument/instrument.category singleton, value=int >= 1
        """
        if res := self.get_info('Instrumentation'):
            # vals: the values passed to create method
            # instrument_vals: a special value that will be pop() on create override to automatically create a work version with instrumentation
            vals = {}
            instrument_vals = defaultdict(int)

            # Split in two steps: First the line breaks, then the commas
            a = res.split("\n")
            c = []
            for b in a:
                c += b.split(",")
            instruments = list(map(lambda i: i.strip(), c))
            for i, instrument in enumerate(instruments):
                if m := re.match(r"^(\d+)?\s?([a-zA-Z]+):?\s?(.*)", instrument):
                    m = (m.groups())
                    qty = max(int(m[0]), 1) if m[0] else 1
                    instrument_id = self.env['instrument'].get_from_string(m[1]) or \
                                    self.env['instrument'].get_from_string("%s %s" % (m[1], m[2])) or \
                                    self.env['instrument.category'].get_from_string(m[1])

                    # Handle the 3rd part of the string
                    # If it's a piano piece for "X-hands"
                    if q := re.match(r"(\d\d?)-hands?", m[2]):
                        qty = math.ceil(int((q.groups())[0]) / 2)
                    # If a white space is missing between 2 instruments  (ex: '2 bassoons2 horns')
                    elif m[2] not in ['soli', 'solo'] and re.search(r"^(\d )?[a-zA-Z]+$", m[2]):
                        instruments.insert(i + 1, m[2])
                    # If there is an alternative instrument (ex: 'flute (or violin)')
                    elif re.search(r"\(or ", m[2]):
                        vals.update({'to_check': True, 'to_check_reason': "Alternative versions (%s %s)" % (m[1], m[2])})

                    # Some things to be checked
                    if not instrument_id:
                        vals.update({'to_check': True, 'to_check_reason': "No instrument found for '%s'" % m[1]})
                    elif len(instrument_id) > 1:
                        vals.update({'to_check': True, 'to_check_reason': "Multiple instruments found for '%s'" % m[1]})
                        instrument_id = instrument_id.filtered('is_default')[:1] or instrument_id[:1]


                    if instrument_id:
                        instrument_vals[instrument_id] += qty
                else:
                    vals.update({'to_check': True, 'to_check_reason': "No match for %s" % instrument})

            if instrument_vals:
                vals.update({'original_instrumentation': instrument_vals})
            return vals

        return {}


    # --------------------------------------------
    #                   PARSING
    # --------------------------------------------


    def _get_webpage_infos(self):
        """
        Parse the IMSLP webpage by calling sub-methods to get several types of informations
        Create infos related
        :return:
        """
        self.ensure_one()
        _logger.info("Parsing webpage for %s" % self.name)

        # The key/value pairs
        vals = {}
        self.state = 'parsed'

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
        # We try to get matching composer and work in the database, just in case...
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
                _logger.info("Calling IMSLP api : %s" % url.replace("{{START}}", str(start))[30:])
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

