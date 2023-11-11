{
    'name': "Music Library",
    'description': """
       Music library extension to add an API
    """,

    'license': 'AGPL-3',
    'category': "Uncategorized",
    'version': "17.0.0.0.1",
    'installable': True,
    'application': False,
    'sequence': 1,
    
    'author': "Gautier « MrFaBemol » Casabona",
    'website': "https://www.octoopus.org",
    
    'depends': ['music_library'],
    
    'data': [
        # Views
        'views/api_token.xml',
        'views/api_request.xml',
        'views/music_composer.xml',
        'views/music_instrument.xml',
        'views/music_work.xml',

        # Data
        # 'data/api_token.xml',

        # Security
        'security/ir.model.access.csv',

        # Menus
        'data/menu_items.xml',
    ],

}

