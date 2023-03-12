# -*- coding: utf-8 -*-

{
    'name': "IMSLP integration for Music Library module",
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

        # Views
        'views/imslp_composer.xml',
        'views/imslp_composer_infos.xml',
        'views/imslp_work.xml',
        'views/imslp_work_infos.xml',
        'views/music_composer.xml',
        'views/music_work.xml',

        # Wizards
        # 'wizards/get_composers_wizard.xml',
        # 'wizards/get_works_wizard.xml',

        # Data
        'data/menu_items.xml',
        'data/ir_config_parameter.xml',
        'data/scheduled_actions.xml',

        # Security
        'security/ir.model.access.csv',
    ],

    'qweb': [],
}
