from odoo import api, fields, models, _

class MusicComposer(models.Model):
    _inherit = "music.composer"

    imslp_composer_id = fields.Many2one(comodel_name="imslp.composer", compute="_compute_imslp_composer_id", search="_search_imslp_composer")
    imslp_url = fields.Char(related="imslp_composer_id.url")
    imslp_works = fields.One2many(related="imslp_composer_id.imslp_work_ids")
    imslp_pending_works = fields.Many2many(comodel_name="imslp.work", compute="_compute_imslp_works_infos")
    imslp_pending_works_qty = fields.Integer(compute="_compute_imslp_works_infos")


    def _compute_imslp_composer_id(self):
        for composer in self:
            composer.imslp_composer_id = self.env['imslp.composer'].search([('composer_id', '=', composer.id)], limit=1)

    @api.depends('imslp_composer_id', 'work_ids')
    def _compute_imslp_works_infos(self):
        for composer in self:
            composer.imslp_pending_works = composer.imslp_works.filtered(lambda w: not w.work_id)
            composer.imslp_pending_works_qty = len(composer.imslp_pending_works)

    def _search_imslp_composer(self, operator, value):
        op = "not in" if not value and operator == "=" else "in"
        domain = [("name", "ilike", value)] if value else []
        return [('id', op, self.env['imslp.composer'].search(domain).composer_id.ids)]


    def action_show_imslp_pending_works(self):
        self.ensure_one()
        return {
            "name": _("Pending works for %s" % self.full_name),
            "type": 'ir.actions.act_window',
            "res_model": 'imslp.work',
            "domain": [('id', 'in', self.imslp_works.ids)],
            "views": [[False, "tree"]],
            "context": {
                **self.env.context,
                'search_default_filter_pending': 1,
            }
        }