# -*- coding: utf-8 -*-

{
    'name': "Music Library",
    'description': """
       An app to manage composers and music works
    """,
    'author': 'Gautier Casabona',
    'license': 'LGPL-3',
    'category': "Uncategorized",
    'version': "15.0.0",
    'installable': True,
    'sequence': 1,
    
    'author': "Odoo S.A.",
    'website': "http://www.odoo.com",
    
    'depends': ['web', 'mail'],
    
    'data': [
        'security/ir.model.access.csv',
        'datas/ir_config_parameter.xml',

        'views/composer.xml',
        'wizards/oo_get_composers_wizard.xml',

        'views/menu_items.xml',
    ],
}
