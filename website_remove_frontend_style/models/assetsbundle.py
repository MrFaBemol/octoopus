from odoo.addons.base.models.assetsbundle import StylesheetAsset

def to_node_no_bootstrap(self):
    # [CUST] Need this fix to filter some boostrap shit
    if "bootstrap" in self.url:
        return ("link", {}, None)

    return self.to_node_super()


# [CUST] We need to keep the original to_node() method so we can call it like a "super" method
StylesheetAsset.to_node_super = StylesheetAsset.to_node
StylesheetAsset.to_node = to_node_no_bootstrap
