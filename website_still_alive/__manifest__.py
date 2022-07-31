# -*- coding: utf-8 -*-

{
    'name': "Still alive (Octoopus website)",
    'description': """
        A portal extension for Octoopus. Depends on music_library module 
    """,
    'category': "Website",
    'version': "15.0.0.0.1",
    'installable': True,
    'sequence': 1,

    'license': 'LGPL-3',
    'author': "MrFaBemol",
    'website': "https://www.octoopus.com",

    'depends': [ 'music_library', 'material_ux'],
    "assets": {
        "web.assets_frontend": [
            # 'website_still_alive/static/js/owl.iife.min.js',
            'website_still_alive/static/js/__init__.js',
            'website_still_alive/static/js/tools.js',
            'website_still_alive/static/js/composers.js',
            'website_still_alive/static/js/works.js',


            'website_still_alive/static/css/material_extended.scss',

            'website_still_alive/static/css/colors.scss',
            'website_still_alive/static/css/autocomplete.scss',
            'website_still_alive/static/css/layouts.scss',
            'website_still_alive/static/css/composers.scss',
            'website_still_alive/static/css/works.scss',


        ],
    },

    'data': [
        'data/website_menu.xml',

        'static/xml/homepage.xml',
        'static/xml/what.xml',
    ],

}
