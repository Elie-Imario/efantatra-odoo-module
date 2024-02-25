# -*- coding: utf-8 -*-

from odoo import api, fields, models

class historiqueTraitement(models.Model):
    _name='efantatra.historique.traitement'
    _description='efantatra_historique_traitement'

    date_action = fields.Date()
    action_type = fields.Selection([
        ('action_1','Création'),
        ('action_2','Modification'),
        ('action_3','Suppression')],string="Type d'action")
    user_operant = fields.Char(string="Utilisateur Opérant")
    numero_previsa_traite = fields.Char(string="Numéro Previsa concerné")
    numero_dossier_traite = fields.Char(string="Numéro Dossier concerné")