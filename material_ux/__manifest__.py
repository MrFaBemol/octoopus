# -*- coding: utf-8 -*-

{
    'name': "Material UX for Odoo website",
    'category': "Technical",
    'version': "15.0.0.0.1",
    'installable': True,
    'sequence': 1,

    'license': "LGPL-3",
    'author': "MrFaBemol",
    'website': "https://www.odoo.com",

    'depends': ['website'],
    "assets": {
        "web.assets_frontend": [
            # Javascript
            "material_ux/static/js/__init__.js",

            # Scss
            "material_ux/static/css/colors_material.scss",
            "material_ux/static/css/colors.scss",
            "material_ux/static/css/global.scss",

            "material_ux/static/css/components/*",

        ],
    },

    'data': [],
    'qweb': [],
}
