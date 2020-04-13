# Copyright 2020 Tomeyro
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'Turnip Tracker',
    'summary': '''Module to track turnip prices.''',
    'author': 'Tomeyro',
    'website': 'https://github.com/tomeyro',
    'license': 'AGPL-3',
    'category': 'Tools',
    'version': '12.0.1.0.01',
    'depends': [
        'website',
        'portal',
    ],
    'test': [
    ],
    'data': [
        'security/ir.model.access.csv',

        'views/turnip_island.xml',
        'views/turnip_price.xml',

        'views/assets.xml',
        'views/turnip_menus.xml',

        'templates/turnip_portal.xml',
        'templates/turnip_tracker.xml',
    ],
    'demo': [
    ],
    'external_dependencies': {
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}
