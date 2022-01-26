# -*- coding: utf-8 -*-

{
    'name': "Music Library",
    'description': """
       An app to manage composers and music works
    """,
    'author': 'Gautier Casabona',
    'license': 'LGPL-3',
    'category': "Uncategorized",
    'version': "15.0.0.1.2",
    'installable': True,
    'sequence': 1,
    
    'author': "Odoo S.A.",
    'website': "http://www.odoo.com",
    
    'depends': ['web', 'mail', 'portal'],
    
    'data': [
        'datas/ir_config_parameter.xml',
        'datas/music_note.xml',
        'datas/api_token.xml',

        'views/composer.xml',
        'views/music_work.xml',
        'views/instrument_category.xml',
        'views/instrument.xml',
        'views/music_note.xml',
        'views/period.xml',

        'views/api_token.xml',
        'views/api_request.xml',

        'wizards/oo_get_composers_wizard.xml',
        'wizards/oo_get_works_wizard.xml',
        'wizards/update_tonality_wizard.xml',

        'views/menu_items.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
}
