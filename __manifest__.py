# -*- coding: utf-8 -*-
{
    'name': "openacademy",

    'summary': """Learning Managment System just for learning Purpos""",

    'description': """ Write Some Discription About this module here""",

    'author': "Abdul Shakoor",
    'website': "http://www.yourcompany.com",
    'category': 'Education Institute',
    'version': '1.0.0',
    'sequence': -100,
    'lecince': 'LPG-15',

    # application true use for k ap k filetrr main app lekha ho to b module search ho jahy
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list

    'installable': True,
    'application': True,
    'auto_install': False,
    # any module necessary for this one to work correctly
    # dapands is use for inherat some other module in our modules
    'depends': ['base', 'board'],

    # always loaded
    # data [] it is use to import the XML files
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/add_attend_wizard.xml',
        'views/course.xml',
        'views/session.xml',
        'views/partner.xml',
        'views/session_board.xml',
        'data/data.xml',
        'report/report.xml',

    ],
    # only loaded in demonstration mode  or impor demo data files
    'demo': [
        'demo/demo.xml',
    ],

}
