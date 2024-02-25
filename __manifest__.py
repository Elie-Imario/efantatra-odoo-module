# -*- coding: utf-8 -*-
{
    'name': "efantatra",
    'summary': """
        Un module permettant de faire le suivis des dossiers de la circonscription
        domainiale d'Avaradrano""",

    'description': """
        Cet module offre de meilleur facilité de suivis et de traitement des dossiers
    """,
    'author': "Imarioa",
    'website': "http://odoo-skills.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/email_template.xml',
        'data/cron_action.xml',
        'views/pvFrontView.xml',
        'views/pvFront_ChefView.xml',
        'views/dossierFrontView.xml',
        'views/dossierFront_ChefView.xml',
        'views/pv_extendFormViews.xml',
        'views/oe_chatter.xml',
        'views/usageFrontView.xml',
        'views/bureauFrontView.xml',
        'views/historique_traitement.xml',
        'views/graph_view.xml',
        'wizard/sendEmailTemplateForm.xml',
        'wizard/sendSMSTemplateForm.xml',
        'views/resusers.xml',
        'views/menu.xml',
        'report/dossierReportTemplate.xml',
        'report/dossierReport.xml',
        'report/PVReportTemplate.xml',
        'report/PVReport.xml',
    ],
    'assets': {
        "web.assets_backend": [
            'efantatra/static/src/scss/_dossier.scss',
            'efantatra/static/src/scss/_usage_card.scss',
            'efantatra/static/src/js/basic_views.js',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application' : True,
}
