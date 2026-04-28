{
    "name": "Choice of Practices",
    "maintainer": 'Cherednyk Matvii',
    "version": "15.0",
    "depends": ['base', 'alnas_xlsx','contacts','utm',  'web_notify'],
    "data": [
        'reports/reports_templates.xml',

        'demo/partner_demo_data.xml',
        'demo/enterprises_demo.xml',


        'data/institutes_data.xml',
        'data/student_group_data.xml',
        'data/ir_cron_data.xml',
        'data/education_programs_data.xml',
        'data/departments_data.xml',
        'data/sequence.xml',
        'wizard/partner_check_wizard.xml',
        'views/enterprises_views.xml',
        'views/practice_agreement_views.xml',
        'views/practice_request_views.xml',
        'views/res_partner_views.xml',
        'views/placement_practical_views.xml',
        'views/student_group_views.xml',
        'views/education_program_views.xml',
        'views/signup_templates.xml',
        'views/departments_views.xml',
        'views/institutes_views.xml',
        'security/role_group.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',

        'views/menu.xml',
        'views/rewrite_menu.xml'
    ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'chm_choice_of_practices/static/src/js/xlsx_print_button.js',
    #     ],
    # },

    "application": True,
    "installable": True,

}
