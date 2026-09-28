{
    'name': 'AI Speech Therapy',
    'version': '1.0',
    'category': 'Education',
    'summary': 'AI-assisted speech therapy for children',
    'description': """
        AI Speech Therapy
        =================

        A speech therapy management application for children.
    """,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/child_views.xml',
        'views/exercise_views.xml',
        'views/session_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
}