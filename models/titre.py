from odoo import models, fields, api


class titre(models.Model):
    _inherit = ['efantatra.dossier']

    indice_titre = fields.Integer("Titre N°") 
    t_num = fields.Char()
    ppt =  fields.Char("Proprieté dite")
    duplicata = fields.Selection([
        ('f', 'sans duplicata'),
        ('t', 'avec duplicata'),
        ])