{
    'name': 'Still alive theme',
    'description': 'The Octoopus default theme',
    'version': '15.0.0.0.1',
    'author': 'MrFaBemol',
    'license': 'LGPL-3',
    'category': 'Theme/Education',

    'depends': ['website_still_alive'],
    'data': [
        'views/layout.xml',
    ],

    "assets": {
        "web.assets_frontend": [
            # Javascript
            "theme_still_alive/static/js/__init__.js",

            # Scss
            "theme_still_alive/static/css/colors.scss",
            "theme_still_alive/static/css/global.scss",
            "theme_still_alive/static/css/layout.scss",

        ],
    },
}
