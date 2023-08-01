# -*- coding: utf-8 -*-

{
    'name': "Octoopus website",
    'description': """
        A portal extension for Octoopus.
        Depends mainly on music_library & website_remove_bootstrap module 
    """,
    'category': "Website",
    'version': "16.0.1.0.0",
    'installable': True,
    'sequence': 1,

    'license': 'OPL-1',
    'author': "MrFaBemol",
    'website': "https://www.mrfabemol.com",

    'depends': ['music_library', 'website_remove_frontend_style'],
    "assets": {
        "web.assets_frontend": [
            # External libraries
            'website_octoopus/static/lib/tailwind-3.3.0.js',
            # 'website_octoopus/static/lib/tailwind_build.css',
            'website_octoopus/static/lib/flowbite.min.css',
            # 'website_octoopus/static/lib/flowbite.min.js',

            # 'website_octoopus/static/css/main.css',
            'website_octoopus/static/src/js/owl.js',
            'website_octoopus/static/src/js/tools.js',

            'website_octoopus/static/src/js/dynamic_placeholder_input/component.js',
            'website_octoopus/static/src/js/dynamic_placeholder_input/template.xml',
            'website_octoopus/static/src/js/main_search_bar/component.js',
            'website_octoopus/static/src/js/main_search_bar/template.xml',
            # 'website_octoopus/static/js/composers.js',
            # 'website_still_alive/static/js/works.js',


            # 'website_still_alive/static/css/colors.scss',
            # 'website_still_alive/static/css/autocomplete.scss',
            # 'website_still_alive/static/css/layouts.scss',
            # 'website_still_alive/static/css/composers.scss',
            # 'website_still_alive/static/css/works.scss',

            '/website_octoopus/static/lib/flowbite.min.js',

        ],
    },

    'data': [
        'data/website_menu.xml',

        'static/src/xml/layout.xml',
        'static/src/xml/homepage.xml',
        # 'static/xml/what.xml',
    ],

}
