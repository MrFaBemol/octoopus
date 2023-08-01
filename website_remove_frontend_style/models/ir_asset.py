from odoo import models


class IrAsset(models.Model):
    _inherit = "ir.asset"

    def _get_asset_paths(self, bundle, addons=None, css=False, js=False):
        res = super(IrAsset, self)._get_asset_paths(bundle, addons, css, js)
        if 'frontend' in bundle:
            res = list(filter(lambda t: t[0][-3:] != "css", res))
        return res
