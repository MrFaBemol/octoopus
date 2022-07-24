# -*- coding: utf-8 -*-

{
    'name': "Material UX for Odoo website",
    'category': "Technical",
    'version': "15.0.0.0.1",
    'installable': True,
    'sequence': 1,

    'license': "OEEL-1",
    'author': "Odoo PS",
    'website': "http://www.odoo.com",

    'depends': ['website'],
    "assets": {
        "web.assets_frontend": [
            "material_ux/static/css/colors.scss",
            "material_ux/static/css/global.scss",
            "material_ux/static/css/form.scss",


            "material_ux/static/js/init.js",
        ],
    },

    'data': [],

    'qweb': [],
}
