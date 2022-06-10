# -*- coding: utf-8 -*-

{
    'name': "Music Library",
    'description': """
       An app to manage composers and music works
    """,

    'license': 'LGPL-3',
    'category': "Uncategorized",
    'version': "15.0.0.1.5",
    'installable': True,
    'sequence': 1,
    
    'author': "MrFaBemol",
    'website': "http://www.octoopus.com",
    
    'depends': ['web', 'mail', 'portal'],
    'external_dependencies': {'python': ['beautifulsoup4']},
    
    'data': [
        'datas/ir_config_parameter.xml',
        'datas/scheduled_actions.xml',
        'datas/music_note.xml',
        'datas/api_token.xml',

        'views/composer.xml',
        'views/music_work.xml',
        'views/music_work_version.xml',
        'views/music_work_version_instrument.xml',
        'views/instrument.xml',
        'views/instrument_category.xml',
        'views/music_note.xml',
        'views/period.xml',

        'views/api_token.xml',
        'views/api_request.xml',
        'views/imslp_composer.xml',
        'views/imslp_composer_infos.xml',
        'views/imslp_work.xml',
        'views/imslp_work_infos.xml',

        'wizards/oo_get_composers_wizard.xml',
        'wizards/oo_get_works_wizard.xml',
        'wizards/update_tonality_wizard.xml',
        'wizards/create_work_version_wizard.xml',

        'views/menu_items.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
}
