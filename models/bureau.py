# -*- coding: utf-8 -*-

from odoo import api, fields, models

class bureau(models.Model):
    _name='efantatra.bureau'
    _rec_name = 'libelle_bureau'

    libelle_bureau = fields.Char("Libelle")
    bureau_name = fields.Char("Nom du bureau")
    nbpersonnel = fields.Integer("Nombre de Personnel")