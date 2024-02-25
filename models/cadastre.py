from odoo import models, fields, api


class cadastre(models.Model):
    _inherit = ['efantatra.dossier']

    parcelle = fields.Char("Parcelle")
    section = fields.Char("Section")
    folio = fields.Integer("Folio")
    registre = fields.Integer("Registre")
    commune = fields.Char("Commune")
    extrait_matriciel = fields.Selection([
        ('f', 'sans extrait'),
        ('t', 'avec extrait'),
        ]) 