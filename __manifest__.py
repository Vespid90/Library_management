# -*- coding: utf-8 -*-
{
    'name': "my_library",

    'summary': "Summary of library",

    'description': """
Librairie de livres
    """,

    'author': "Vespid",
    'license': "LGPL-3",
    'website': "https://www.fafasburger.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Library',
    'version': '0.1',
    'post_init_hook': 'duration_loan',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/group_security.xml',
        'security/ir.model.access.csv',

        'views/library_book_view.xml',
        'views/library_loan_view.xml',
        'views/library_member_view.xml',
        'views/book_tag_view.xml',
        'views/book_category_view.xml',
        'views/res_partner_views.xml',
        'views/res_config_settings.xml',

        'data/ir_cron_library.xml',
        'data/my_library_sequence.xml',

        'wizard/library_loan_wizard_view.xml',

        'report/my_library_report.xml',
        'report/member_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': True,
    'sequence': -100,
}
