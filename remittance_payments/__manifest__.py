# -*- coding: utf-8 -*-
{
    'name': "remittance_payments",
    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com
    """,
    'description': """
        Long description of module's purpose
    """,
    'author': "onDevelopSA",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','account'],
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'views/payment_view.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
