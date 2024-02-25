from odoo import models, fields, api
from random import *
import logging

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):	
    _inherit = 'res.users'	
    bureau_Id = fields.Many2one("efantatra.bureau", "Bureau")
    libelle_bureau_user = fields.Char()
    num_matricule = fields.Char()
    
    def getNbutilisateur(self, _libelle_bureau):
        self.env.cr.execute(f"select COUNT(login) as nbPersonnel FROM res_users WHERE libelle_bureau_user = '{_libelle_bureau}'")
        try:
            NbUtilsateur = self.env.cr.fetchone()[0]
        except Exception as e:
            NbUtilsateur = 0

        return NbUtilsateur

    def getOldBureau(self):
        self.env.cr.execute(f"select libelle_bureau_user FROM res_users WHERE id = '{self.id}'")
        libelleBureau = self.env.cr.fetchone()[0]
        return libelleBureau

    def updateNbPersonnel(self,_new_bureau,_action):
        if _action == "CREATE":
            _nbPersonnel_new_bureau = self.getNbutilisateur(_new_bureau)
            self.env.cr.execute(f"update efantatra_bureau set nbpersonnel={_nbPersonnel_new_bureau} WHERE libelle_bureau='{_new_bureau}'")
            
        elif _action == "WRITE":
            _oldbureau = self.getOldBureau()
            _nbPersonnel_old_bureau = self.getNbutilisateur(_oldbureau)
            _nbPersonnel_new_bureau = self.getNbutilisateur(_new_bureau)
    
            if _oldbureau != _new_bureau:
                self.env.cr.execute(f"update efantatra_bureau set nbpersonnel={_nbPersonnel_new_bureau+1} WHERE libelle_bureau='{_new_bureau}'")
                self.env.cr.execute(f"update efantatra_bureau set nbpersonnel={_nbPersonnel_old_bureau-1} WHERE libelle_bureau='{_oldbureau}'")
            else:
                pass
        
        elif _action == "DELETE":
            _nbPersonnel_bureau = self.getNbutilisateur(_new_bureau)
            self.env.cr.execute(f"update efantatra_bureau set nbpersonnel={_nbPersonnel_bureau-1} WHERE libelle_bureau='{_new_bureau}'")
            
        self.env.cr.commit()
     
    def getBureau(self,vals):
        if vals.get('libelle_bureau_user') :
            x = vals.get('libelle_bureau_user')
        elif vals.get('libelle_bureau_user') == False:
            x = False
        else:
            x = self.libelle_bureau_user
        return x

    # def getNumMatriculeUser(self):
    #     self.env.cr.execute(f"SELECT num_matricule FROM res_users")
    #     try:
    #         num_maticule_list = self.env.cr.fetchall()
    #     except Exception as e:
    #         num_maticule_list = None
    #   return num_maticule_list

    @api.onchange("bureau_Id")
    def onchange_bureau_Id(self):
        self.libelle_bureau_user = self.bureau_Id.libelle_bureau

    @api.model
    def create(self, vals):
        rtn = super(ResUsers,self).create(vals)
        self.updateNbPersonnel(vals['libelle_bureau_user'], "CREATE")
        return rtn
    
    def write(self, vals):
        rtn = super(ResUsers,self).write(vals)
        bureau = self.getBureau(vals)        
        if bureau:
            self.updateNbPersonnel(bureau, "WRITE")
        else:
            pass
        return rtn

    def unlink(self):
        try:
            for i in range(0, len(self.ids)):
                user = self.env['res.users'].sudo().search([('id', '=', self.ids[i])])
                self.updateNbPersonnel(user.libelle_bureau_user, "DELETE")
            
            super().unlink()
        except Exception as e:
            _logger.error("Une erreur s'est produite lors de la supression de l'utilisateur!")
                        
        return True
    