from random import randint

# A dict{int: str} to match material colors names with Odoo color picker
# key = the index in odoo color picker
# value = a material color name

MATERIAL_COLORS = {
    1: 'deep-orange',
    2: 'orange',
    3: 'amber',
    4: 'cyan',
    5: 'brown',
    6: 'pink',
    7: 'teal',
    8: 'blue',
    9: 'red',
    10: 'green',
    11: 'purple',

    # Other possible colors
        # 'deep-purple',
        # 'indigo',
        # 'light-blue',
        # 'light-green',
        # 'grey',
        # 'blue-grey'
}

# The material color to use when no color is selected in Odoo.
DEFAULT_MATERIAL_COLOR = 'blue-grey'


def get_odoo_default_color(dummy):
    return randint(1, 11)
