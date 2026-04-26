{
    'name': 'Signup Email Verification',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Підтвердження емейлу',
    'depends': ['base', 'website', 'auth_signup', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/registration_templates.xml',
    ],
    'installable': True,
    'application': False,
}