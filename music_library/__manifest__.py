{
    'name': "Music Library",
    'description': """
       An app to manage composers and music works
    """,

    'license': 'AGPL-3',
    'category': "Uncategorized",
    'version': "17.0.0.1.5",
    'installable': True,
    'application': True,
    'sequence': 1,
    
    'author': "Gautier « MrFaBemol » Casabona",
    'website': "https://www.octoopus.org",
    
    'depends': ['web', 'mail'],
    'external_dependencies': {'python': ['unidecode']},

    "assets": {
        "web.assets_common": [
            'music_library/static/src/css/style.scss',
        ],
    },
    
    'data': [
        # Security
        'security/security.xml',
        'security/ir.model.access.csv',

        # Views
        'views/music_composer.xml',
        'views/music_instrument.xml',
        'views/music_note.xml',
        'views/music_period.xml',
        'views/music_work.xml',
        'views/music_work_version.xml',
        'views/music_work_version_instrument.xml',
        'views/res_config_settings.xml',

        # Wizards
        'wizards/create_work_version_wizard.xml',
        'wizards/update_tonality_wizard.xml',

        # Data
        'data/music_note.xml',              # Need music note before to be used in music_instrument
        'data/music_instrument.xml',


        # Menus
        'data/menu_items.xml',
    ],

}

