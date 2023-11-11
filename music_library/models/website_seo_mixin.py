from odoo import api, fields, models
from odoo.addons.music_library.utils.misc import slugged


class WebsiteSeoMixin(models.AbstractModel):
    _name = "website.seo.mixin"
    _description = "website.seo.mixin"

    # Web
    seo_name = fields.Char(compute="_compute_seo_name")
    slug_url = fields.Char(compute="_compute_slug_url")

    @api.depends('display_name')
    def _compute_seo_name(self):
        """ This should be overriden to compute the real seo_name """
        for record in self:
            record.seo_name = record.display_name if record.id else ""

    @api.depends('seo_name')
    def _compute_slug_url(self):
        for record in self:
            record.slug_url = slugged(record) if record.id else ""
