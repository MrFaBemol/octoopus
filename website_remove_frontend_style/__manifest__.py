# -*- coding: utf-8 -*-

{
    'name': "Remove front styles (especially BootStrap)",
    'category': "Hidden/Tools",
    'version': "16.0.1.0.0",
    'installable': True,
    'sequence': 1,
    
    'license': "GPL-3",
    'author': "MrFaBemol",
    'website': "https://www.mrfabemol.com",
    
    'depends': ['website'],
    "assets": {
        "web.assets_frontend": [
            ('remove', '/web/static/src/legacy/js/core/dialog.js'),
            ('remove', '/web/static/lib/tempusdominus/tempusdominus.scss'),
            ('remove', '/web/static/lib/tempusdominus/tempusdominus.js'),
            ('remove', '/web/static/src/legacy/scss/tempusdominus_overridden.scss'),
            ('remove', '/web/static/src/scss/utilities_custom.scss'),
        ],
    },


}
