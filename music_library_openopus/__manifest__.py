

{
    'name': "OpenOpus integration for Music Library module",
    'category': "Extra Tools",
    'version': "17.0.0.0.1",
    'installable': True,
    'sequence': 1,

    'license': "AGPL-3",
    'author': "Gautier « MrFaBemol » Casabona",
    'website': "https://www.octoopus.org",

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

        # Security
        'security/ir.model.access.csv'
    ],

    'qweb': [],
}
