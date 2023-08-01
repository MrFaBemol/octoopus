from odoo import models


class IrQweb(models.AbstractModel):
    _inherit = "ir.qweb"

    def _get_asset_bundle(self, xmlid, files, env=None, css=True, js=True):
        if "frontend" in xmlid:
            files = list(filter(lambda f: 'bootstrap' not in f['url'] and 'bootstrap' not in f['filename'], files))
        return super(IrQweb, self)._get_asset_bundle(xmlid, files, env, css, js)
