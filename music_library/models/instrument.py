# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Instrument(models.Model):
    _name = "instrument"
    _description = "An instrument"
    _parent_store = True
    _order = 'display_name'

    sequence = fields.Integer(default=10)

    name = fields.Char(required=True, translate=True)
    display_name = fields.Char(compute="_compute_display_name", store=True)
    extra_name_ids = fields.One2many(comodel_name="instrument.extra.name", inverse_name="instrument_id")
    icon = fields.Binary()
    parent_path = fields.Char(index=True)
    parent_id = fields.Many2one(comodel_name="instrument", string="Category", ondelete='restrict')
    child_ids = fields.One2many(comodel_name="instrument", inverse_name="parent_id", string="Instruments")
    is_category = fields.Boolean(compute="_compute_is_category", store=True)

    all_instrument_ids = fields.Many2many(comodel_name="instrument", compute="_compute_all_instrument_ids")
    instrument_qty = fields.Integer(compute="_compute_all_instrument_ids")

    def _get_default_key(self):
        return self.env.ref('music_library.music_note_c').id or False

    key = fields.Many2one(comodel_name="music.note", required=True, default=_get_default_key)
    is_default = fields.Boolean(help="When 2 results are found on automatic creation, take the default instrument")
    is_ensemble = fields.Boolean(string="Is ensemble")
    is_accompaniment = fields.Boolean(string="Is accompaniment")
    accompanist_qty = fields.Integer()

    work_version_ids = fields.Many2many(comodel_name="music.work.version", relation="instrument_version_rel", compute="_compute_work_version_ids")
    work_version_qty = fields.Integer(compute="_compute_work_version_ids")



    # --------------------------------------------
    #                   COMPUTE
    # --------------------------------------------


    @api.depends('name', 'parent_id', 'key')
    def _compute_display_name(self):
        for ins in self:
            if not ins.parent_id:
                ins.display_name = ins.name
                continue
            display_name = "/".join([self.browse(int(i)).name for i in ins.parent_path.split("/")[1:-1]])
            if ins.key != self.env.ref('music_library.music_note_c'):
                display_name += f" ({ins.key.name})"
            ins.display_name = display_name

    @api.depends('child_ids')
    def _compute_is_category(self):
        for instrument in self:
            instrument.is_category = bool(instrument.child_ids)

    @api.depends('child_ids')
    def _compute_all_instrument_ids(self):
        for ins in self:
            ins.child_ids._compute_all_instrument_ids()
            ins.all_instrument_ids = (ins.child_ids.all_instrument_ids | ins.child_ids).filtered(lambda c: not c.is_category)
            ins.instrument_qty = len(ins.all_instrument_ids)

    def _compute_work_version_ids(self):
        for rec in self:
            rec.work_version_ids = self.env['music.work.version.instrument'].search([('instrument_id', '=', rec.id)]).work_version_id.ids
            rec.work_version_qty = len(rec.work_version_ids)


    # --------------------------------------------
    #                   STANDARD
    # --------------------------------------------


    def write(self, vals):
        res = super(Instrument, self).write(vals)
        if 'name' in vals:
            self.env['music.work.version.instrument'].search([('instrument_id', 'in', self.ids)])._compute_name()
        return res


    def name_get(self):
        res = []
        for instrument in self:
            res.append((instrument.id, instrument.name))
        return res



    # --------------------------------------------
    #                   MISC
    # --------------------------------------------


    def get_from_string(self, string, check_plural=True):
        instrument = self.search(['|', ('name', '=ilike', string), ('extra_name_ids.name', '=ilike', string)]).exists()
        if not instrument and check_plural:
            pl_string = string[:-1] if string[-1].lower() == "s" else string + "s"
            instrument = self.search(['|', ('name', '=ilike', pl_string), ('extra_name_ids.name', '=ilike', pl_string)]).exists()
        return instrument


    def get_all_ids(self, with_parents=True, with_childs=True):
        self.ensure_one()
        ids = [self.id]
        if with_parents:
            ids += [int(i) for i in self.parent_path.split("/")[:-2]]
        if with_childs:
            ids += self.all_instrument_ids.ids
        return ids


    # --------------------------------------------
    #                   ACTIONS
    # --------------------------------------------

    def action_open_versions_list(self):
        self.ensure_one()
        return {
            "name": _("All works versions for %s" % self.name),
            "type": 'ir.actions.act_window',
            "res_model": 'music.work.version',
            "views": [[False, "tree"], [False, "form"]],
            "target": 'current',
            "domain": [('id', 'in', self.work_version_ids.ids)],
            "context": {
                **self.env.context,
                'search_default_filter_group_by_composer_id': 0,
            },
        }
