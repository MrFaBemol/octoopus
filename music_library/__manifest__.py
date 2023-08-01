# -*- coding: utf-8 -*-

{
    'name': "Music Library",
    'description': """
       An app to manage composers and music works
    """,

    'license': 'LGPL-3',
    'category': "Uncategorized",
    'version': "16.0.0.1.5",
    'installable': True,
    'application': True,
    'sequence': 1,
    
    'author': "MrFaBemol",
    'website': "https://www.octoopus.com",
    
    'depends': ['web', 'mail', 'portal', "website"],
    'external_dependencies': {'python': ['beautifulsoup4', 'unidecode']},

    "assets": {
        "web.assets_common": [
            'music_library/static/src/css/style.scss',
        ],
        # 'web._assets_frontend_helpers': [
        #     ('remove', 'web/static/src/scss/bootstrap_overridden_frontend.scss'),
        #     ('remove', 'portal/static/src/scss/bootstrap_overridden.scss'),
        # ],

        'web.assets_frontend': [
            # Web
            # ('remove', 'web/static/src/scss/*'),

            # ('remove', 'web/static/lib/bootstrap/scss/**/*'),



            # Portal
            # ('remove', 'portal/static/src/scss/*'),
        ],
    },
    
    'data': [

        # Views
        'views/api_token.xml',
        'views/api_request.xml',
        'views/music_composer.xml',
        'views/music_instrument.xml',
        'views/music_note.xml',
        'views/music_period.xml',
        'views/music_work.xml',
        'views/music_work_version.xml',
        'views/music_work_version_instrument.xml',
        'views/assets.xml',

        # Wizards
        'wizards/create_work_version_wizard.xml',
        'wizards/update_tonality_wizard.xml',

        # Data
        'data/api_token.xml',
        'data/music_note.xml',              # Need music note before to be used in music_instrument
        'data/music_instrument.xml',
        'data/menu_items.xml',

        # Security
        'security/security.xml',
        'security/ir.model.access.csv',
    ],

}


# def to_node(self, css=True, js=True, debug=False, async_load=False, defer_load=False, lazy_load=False):
#     """
#     :returns [(tagName, attributes, content)] if the tag is auto close
#     """
#     response = []
#     is_debug_assets = debug and 'assets' in debug
#     if css and self.stylesheets:
#         css_attachments = self.css(is_minified=not is_debug_assets) or []
#         for attachment in css_attachments:
#             if is_debug_assets:
#                 href = self.get_debug_asset_url(extra='rtl/' if self.user_direction == 'rtl' else '',
#                                                 name=css_attachments.name,
#                                                 extension='')
#             else:
#                 href = attachment.url
#             attr = dict([
#                 ["type", "text/css"],
#                 ["rel", "stylesheet"],
#                 ["href", href],
#                 ['data-asset-bundle', self.name],
#                 ['data-asset-version', self.version],
#             ])
#             response.append(("link", attr, None))
#         if self.css_errors:
#             msg = '\n'.join(self.css_errors)
#             response.append(JavascriptAsset(self, inline=self.dialog_message(msg)).to_node())
#             response.append(StylesheetAsset(self, url="/web/static/lib/bootstrap/dist/css/bootstrap.css").to_node())
#
#     if js and self.javascripts:
#         js_attachment = self.js(is_minified=not is_debug_assets)
#         src = self.get_debug_asset_url(name=js_attachment.name, extension='') if is_debug_assets else js_attachment[0].url
#         attr = dict([
#             ["async", "async" if async_load else None],
#             ["defer", "defer" if defer_load or lazy_load else None],
#             ["type", "text/javascript"],
#             ["data-src" if lazy_load else "src", src],
#             ['data-asset-bundle', self.name],
#             ['data-asset-version', self.version],
#         ])
#         response.append(("script", attr, None))
#
#     return response



# ('link', {'type': 'text/css', 'rel': 'stylesheet', 'href': '/web/static/lib/bootstrap/dist/css/bootstrap.css', 'media': None, 'data-asset-bundle': 'web.assets_frontend', 'data-asset-version': 'f3ed653'}, None)

