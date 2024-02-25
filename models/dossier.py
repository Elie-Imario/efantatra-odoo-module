from odoo import models, fields, api
from odoo.fields import Datetime
from datetime import datetime

import qrcode
import base64
import io
import logging

_logger = logging.getLogger(__name__)

class dossier(models.Model):
    _name = 'efantatra.dossier'
    _description = 'efantatra_dossier'
    _inherit = ['mail.thread']
    _rec_name = 'id'
   
    num_PV = fields.Char("N° PV")
    observation_pv =  fields.Text("Observation PV", tracking=True)
    status = fields.Boolean("Status", default=False)
    visa = fields.Selection([
        ('non_visé', 'en cours'),
        ('visé', 'visé'),
        ], default= 'non_visé',required=True)
    montant_paiement = fields.Integer("Montant") 
    type_dos = fields.Selection([
        ('_type1', 'Titre'),
        ('_type2', 'Cadastre')
    ], "Type Dossier")

    """Dossier Field"""
    indice_Dossier = fields.Char("Indice Dossier")
    num_Dossier = fields.Char("N° Dossier")
    observation_dos = fields.Text("Observation Dossier", tracking=True)
    signe = fields.Selection([
        ('non_signé', 'non signé'),
        ('signé', 'signé'),
        ], default= 'non_signé',required=True)
    date_final = fields.Date()
    duree_detention = fields.Integer(default = 0) 
    qrcode_PV = fields.Image(string="Code QR PV")
    qrcode_DOS = fields.Image(string="Code QR PV")
    dispatcheur = fields.Char()
    date_Dispatch = fields.Date()

    """ dossier && bureau """
    bureau_traitement = fields.Char(default=lambda self : self.env.user.bureau_Id.libelle_bureau)
    """ dossier && usage relation """
    usage = fields.Many2one("efantatra.usage", "Nom deposant")
    usage_name = fields.Char()
    """ dossier && user relation """
    user_id = fields.Many2one("res.users", string="Initiateur", default=lambda self: self.env.user)
    responsable_id = fields.Many2one("res.users", string="Responsable", domain='[("groups_id","in", [40,42]),("libelle_bureau_user","=",bureau_traitement)]',default="")
    
    def getLastInsertId(self):
        self.env.cr.execute(f"select id as Last_Id_Dossier from efantatra_dossier order by id desc limit 1")
        try:
            lastId = int(self.env.cr.fetchone()[0])
        except Exception as e:
            lastId = 0

        return lastId

    def generateNumPV(self, _id):#length 5
        if _id < 9 :
            _num = f"000{str(_id + 1)}"
        elif _id < 99:
            _num = f"00{str(_id + 1)}"
        elif _id < 999:
            _num = f"0{str(_id + 1)}"
        else:
            _num = f"{str(_id + 1)}"
        return _num

    def getpayement(self,vals):
        if vals.get('montant_paiement') :
            x = vals.get('montant_paiement')
        elif vals.get('montant_paiement') == 0:
            x = 0
        else:
            x = self.montant_paiement
        return x

    def generatePVQrCode(self, _typeAction, vals): # 1=Add / 2=EDIT        
        if _typeAction == 1:
            imgQr_PV = qrcode.make(f"""
            N° Pré-Visa : {vals['num_PV']}\n 
            Nom du déposant : {vals['usage_name']}\n 
            Date de dépot : {Datetime.today().strftime('%d/%m/%Y')}\n 
            Agent traitant : {self.env.user.name}\n 
            VISA : En attente de VISA\n 
            """)
            result = io.BytesIO()
            imgQr_PV.save(result, format='PNG')
            result.seek(0)
            img_bytes = result.read()
            base64_encoded_result_bytes = base64.b64encode(img_bytes)
            QRCode = base64_encoded_result_bytes.decode('ascii')
        else:
            imgQr_PV = qrcode.make(f"""
            N° Pré-Visa : {self.num_PV}\n 
            Nom du déposant : {self.usage_name}\n 
            Date de dépot : {self.create_date.strftime('%d/%m/%Y')}\n 
            Agent traitant : {self.user_id.name}\n 
            VISA : VISA accordé\n
            """)
            result = io.BytesIO()
            imgQr_PV.save(result, format='PNG')
            result.seek(0)
            img_bytes = result.read()
            base64_encoded_result_bytes = base64.b64encode(img_bytes)
            QRCode = base64_encoded_result_bytes.decode('ascii')
                    
        return QRCode

    def generateDOSQRCode(self, _actiontype, vals): #1=add NuméroDossier #2=Edit dossier
        if _actiontype == 1:
            imgQr_Dos = qrcode.make(f"""
            N° Dossier : {vals['num_Dossier']}\n 
            Nom du déposant : {self.usage_name}\n
            Responsable du dossier : {self.env['res.users'].sudo().search([('id', '=', vals['responsable_id'])]).name}\n
            Signature: En attente de Signature\n
            """)
            result = io.BytesIO()
            imgQr_Dos.save(result, format='PNG')
            result.seek(0)
            img_bytes = result.read()
            base64_encoded_result_bytes = base64.b64encode(img_bytes)
            QRCode = base64_encoded_result_bytes.decode('ascii')
        else:
            imgQr_Dos = qrcode.make(f"""
            N° Dossier : {self.num_Dossier}\n 
            Nom du déposant : {self.usage_name}\n
            Traité par : {self.responsable_id.name}\n            
            Signature: Dossier signé\n
            Durée de traitement du dossier: {self.duree_detention if self.duree_detention>0 else 1} j\n
            """)
            result = io.BytesIO()
            imgQr_Dos.save(result, format='PNG')
            result.seek(0)
            img_bytes = result.read()
            base64_encoded_result_bytes = base64.b64encode(img_bytes)
            QRCode = base64_encoded_result_bytes.decode('ascii')

        return QRCode

    def print_Dossier(self):
        return self.env.ref('efantatra.report_dossier').report_action(self)

    def print_PV(self):
        return self.env.ref('efantatra.report_PV').report_action(self)

    def save_action(self, _action_type, _vals):
        if _action_type == 'action_1':
            self.env.cr.execute(f"""INSERT INTO efantatra_historique_traitement 
                (date_action,action_type,user_operant,numero_previsa_traite,numero_dossier_traite) 
                VALUES(
                '{Datetime.now()}',
                '{_action_type}',
                '{self.env.user.name}',
                '{_vals['num_PV']}',
                '{""}'
                )
            """)
        elif _action_type == 'action_2':
            self.env.cr.execute(f"""INSERT INTO efantatra_historique_traitement 
                (date_action,action_type,user_operant,numero_previsa_traite,numero_dossier_traite) 
                VALUES(
                '{Datetime.now()}',
                '{_action_type}',
                '{self.env.user.name}',
                '{self.num_PV}',
                '{_vals['num_Dossier'] if _vals['num_Dossier'] else ""}'
                )
            """)
        else:
            self.env.cr.execute(f"""INSERT INTO efantatra_historique_traitement 
                (date_action,action_type,user_operant,numero_previsa_traite,numero_dossier_traite) 
                values  (
                '{Datetime.now()}',
                '{_action_type}',
                '{self.env.user.name}',
                '{_vals.num_PV}',
                '{_vals.num_Dossier if _vals.num_Dossier else ""}'
                )
            """)
        
    def days_between(self, day1, day2):
        d1 = datetime.strptime(str(day1),"%Y-%m-%d")
        d2 = datetime.strptime(str(day2),"%Y-%m-%d")
        return abs((d2 - d1).days)

    def updateDuree_Detention(self, _duree, _id):
        self.env.cr.execute(f"""UPDATE efantatra_dossier SET duree_detention = {_duree} WHERE id = {_id}""")
        
    @api.onchange("usage")
    def onchange_usage(self):
        self.usage_name = self.usage.name_usager

    @api.onchange("responsable_id")
    def onchange_responsable_id(self):
        self.dispatcheur = self.user_id.name
        self.date_Dispatch = Datetime.now()

    @api.onchange("signe")
    def onchange_signe(self):
        self.date_final = Datetime.now()

    @api.model
    def create(self, vals):
        vals['num_PV'] = f"PV {self.generateNumPV(self.getLastInsertId())}/{vals['bureau_traitement']}/{Datetime.now().strftime('%y')} {'T' if vals['type_dos'] == '_type1' else 'C'}"
        vals['t_num'] = f"TN {vals['indice_titre']}-{vals['bureau_traitement']}" if int(vals.get('indice_titre')>0) else False 
        # Creation du code QR    
        vals['qrcode_PV'] = self.generatePVQrCode(1, vals)
        self.save_action('action_1', vals)    
        rtn = super(dossier,self).create(vals)
        return rtn

    def write(self, vals):
        visa = vals.get('visa') if vals.get('visa') else self.visa
        montant = self.getpayement(vals)
        vals['status'] = True if  visa == "visé" and montant > 0  else False
        #generate num_dossier
        indice_dos = vals.get('indice_Dossier') if vals.get('indice_Dossier') else self.indice_Dossier
        vals['num_Dossier'] = f"DOS {indice_dos}/{self.bureau_traitement}/{Datetime.now().strftime('%y')} {'T' if self.type_dos == '_type1' else 'C'}" if indice_dos else False
        #generate newQrPVCode
        if visa == 'visé':
            try:
                vals['qrcode_PV'] = self.generatePVQrCode(2, vals)
            except Exception as e:
                _logger.error("Une erreur s'est produite lors de la génération du QRCode du PV!")
        else:
            try:
                vals['qrcode_PV'] = self.qrcode_PV #for PV
            except Exception as e:
                _logger.error("Une erreur s'est produite lors de la génération du QRCode du PV!")
        
        #generate DosQrCode
        signe = vals.get('signe') if vals.get('signe') else self.signe
        
        if vals.get('indice_Dossier'):
            try:
                vals['qrcode_DOS'] = self.generateDOSQRCode(1, vals)
            except Exception as e:
                _logger.error("Une erreur s'est produite lors de la génération du QRCode du dossier!")
                
        elif signe =='signé':
            try:
                vals['qrcode_DOS'] = self.generateDOSQRCode(2, vals)
            except Exception as e:
                _logger.error("Une erreur s'est produite lors de la génération du QRCode du dossier!")

        else: 
            try:
                vals['qrcode_DOS'] = self.qrcode_DOS
            except Exception as e:
                _logger.error("Une erreur s'est produite lors de la génération du QRCode du dossier!")


        self.save_action('action_2', vals)    
        rtn = super(dossier,self).write(vals)
        return rtn

    def unlink(self):
        try:
            for i in range(0, len(self.ids)):
                dossier = self.env['efantatra.dossier'].sudo().search([('id', '=', self.ids[i])])
                self.save_action('action_3', dossier)
                
            super().unlink()
        except Exception as e:
            _logger.error("Une erreur s'est produite lors de la supression du dossier!")
                    
        
        return True

    @api.model
    def updatesheduledAction(self):
        todayDate = Datetime.today().strftime('%Y-%m-%d')
        dossiers = self.env['efantatra.dossier'].sudo().search([('num_PV', '!=', False)])
        for i in range(0, len(dossiers)):
            if not dossiers[i].date_final:
                dos_create_date = dossiers[i].create_date.strftime('%Y-%m-%d')
                diff_date = self.days_between(dos_create_date, todayDate)
                self.updateDuree_Detention(diff_date, dossiers[i].id)
                