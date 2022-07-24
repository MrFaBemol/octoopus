{
    'name': 'Still alive theme',
    'description': 'The Octoopus default theme',
    'version': '1.0',
    'author': 'MrFaBemol',
    'category': 'Theme/Education',

    'depends': ['website_still_alive'],
    'data': [
        'views/layout.xml',
    ],

    "assets": {
        "web.assets_frontend": [
            "theme_still_alive/static/css/colors.scss",
            "theme_still_alive/static/css/global.scss",
            "theme_still_alive/static/css/layout.scss",

            "theme_still_alive/static/js/hooks.js",
        ],
    },
}
