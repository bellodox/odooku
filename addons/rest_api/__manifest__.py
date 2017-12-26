# -*- coding: utf-8 -*-
{
    'name': 'REST API',
    'version': '1.3.0',
    'category': 'API',
    'author': 'Andrey Sinyanskiy SP',
    'support': 'avs3.ua@gmail.com',
    'license': 'OPL-1',
    'price': 129.00,
    'currency': 'EUR',
    'summary': 'Professional RESTful API access to Odoo models with OAuth2 authentification and Redis token store',
    #'description': < auto-loaded from README file
    'external_dependencies': {
        'python' : ['redis'],
    },
    'depends': [
        'base',
        'web',
    ],
    'data': [
        'data/ir_configparameter_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
