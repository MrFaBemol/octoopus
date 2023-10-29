# -*- coding: utf-8 -*-

{
    'name': "Pretty community",
    'description': "A small module for personal use because I'm used to enterprise version",
    'category': "Design",
    'version': "17.0.0.0.1",
    'installable': True,
    'sequence': 1,

    'license': "LGPL-3",
    'author': "MrFaBemol",
    'website': "https://www.odoo.com",

    'depends': ['web'],
    "assets": {
        "web.assets_backend": [
            "pretty_community/static/src/css/common.css",
        ],
    },

    'data': [],
}
