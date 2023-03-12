# -*- coding: utf-8 -*-

{
    'name': "OpenOpus integration for Music Library module",
    'category': "Extra Tools",
    'version': "16.0.0.0.1",
    'installable': True,
    'sequence': 1,

    'license': "OEEL-1",
    'author': "MrFaBemol",
    'website': "https://www.mrfabemol.com",

    'depends': ['music_library'],
    "assets": {},

    'data': [
        # Data
        'data/ir_config_parameter.xml',

        # Views
        'views/music_composer.xml',
        'views/music_work.xml',

        # Wizards
        'wizards/get_composers_wizard.xml',
        'wizards/get_works_wizard.xml',
    ],

    'qweb': [],
}
