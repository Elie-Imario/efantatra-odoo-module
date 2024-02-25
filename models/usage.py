from odoo import models, fields, api


class usage(models.Model):
    _name = 'efantatra.usage'
    _description = 'efantatra_usage'
    _rec_name = 'name_usager'
    
    name_usager = fields.Char("Nom")
    adresse = fields.Char("Adresse")
    email_adress = fields.Char("Email")
    phone_number = fields.Char("Phone")
    cin = fields.Char("CIN")
    avatar= fields.Image("Photos")

    