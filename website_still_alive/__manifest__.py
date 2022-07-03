# -*- coding: utf-8 -*-

{
    'name': "Still alive (website addon)",
    'description': """
        A portal extension for Octoopus. Depends on music_library module 
    """,
    'category': "Website",
    'version': "15.0.0.0.1",
    'installable': True,
    'sequence': 1,

    'license': 'LGPL-3',
    'author': "MrFaBemol",
    'website': "http://www.octoopus.com",

    'depends': ['website', 'music_library'],
    "assets": {
        # "web.assets_backend": [
        #     'website_still_alive/static/src/qweb/*',
        # ],
        "web.assets_frontend": [
            'website_still_alive/static/src/js/owl.iife.min.js',
            'website_still_alive/static/src/js/tools.js',
            'website_still_alive/static/src/js/material.min.js',
            'website_still_alive/static/src/js/composers.js',
            'website_still_alive/static/src/js/works.js',


            'website_still_alive/static/src/css/material.min.css',
            'website_still_alive/static/src/css/material_extended.scss',

            'website_still_alive/static/src/css/autocomplete.scss',

            # 'website_still_alive/static/src/css/color-variables.scss',
            'website_still_alive/static/src/css/global.scss',
            'website_still_alive/static/src/css/layouts.scss',
            # 'website_still_alive/static/src/css/forms.css',
            'website_still_alive/static/src/css/what.scss',


        ],
        # 'web.assets_qweb': [
        #     'website_still_alive/static/src/qweb/*',
        # ]
    },

    'data': [
        'data/website_menu.xml',

        'static/src/xml/homepage.xml',
        'static/src/xml/what.xml',
        # 'static/src/qweb/*',
    ],

    # 'qweb': [
    #     'static/src/qweb/works.xml',
    # ],
}
