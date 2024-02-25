# -*- coding: utf-8 -*-

from odoo import api, fields, models

class emailWizard(models.TransientModel):
    _name='efantatra.email.wizard'
    _description='efantatra_email_wizard'
    _inherit = ['mail.thread']

    email_body = fields.Text()
    object = fields.Char("Object")
    sender_email_adress = fields.Char("From")
    sending_id = fields.Integer("Id_Usager")
    sending_email_adress = fields.Char("To")

    def getUsagerEmailAdress(self, _id):
        self.env.cr.execute(f"SELECT email_adress FROM efantatra_usage WHERE id={_id}")
        try:
            emailAdress = self.env.cr.fetchone()[0]
        except Exception as e:
            emailAdress = None

        return emailAdress

    def _send_mail(self,_from_email_adress,_object, _to_email_adress, _email_body):
        """ send notification email to usager """
        template = self.env.ref('efantatra.notification_mail_template')
        if not template:
            raise Exception('Impossible de trouver le tepmlate "email_template"')
        
        context = {
            'email_body': _email_body,
            'sender_email': _from_email_adress,
        }
        email_values = {
            'email_cc': False,
            'subject': _object,
            'email_from': _from_email_adress,
            'email_to': _to_email_adress,
            'auto_delete': False,
            'recipient_ids': [],
            'partner_ids': [],
            'scheduled_date': False,
        }
        template.with_context(context).send_mail(self.id,force_send=True, email_values=email_values)
        return True
        
    def success_notification(self, notification_message):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': notification_message,
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }

    def error_notification(self, notification_message):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': notification_message,
                'type': 'danger',
                'sticky': False,
            }
        }

    def isEmail_sent(self, _email_subject):
        sent_mails = self.env['mail.mail'].sudo().search([('subject', '=', _email_subject)], limit=1, order="create_date desc")
        if sent_mails.state == 'sent':
            return True
        else:
            return False
    
    def action_sendEmail(self):
        self._send_mail(self.sender_email_adress,self.object,self.sending_email_adress,self.email_body)
        
        if self.isEmail_sent(self.object):
            show_msg = self.success_notification("L'email a été envoyé avec success")
        else:
            show_msg = self.error_notification("Une exception c'est produite lors de l'envoi, veuillez réessayer! ")

        return show_msg

        

    @api.model
    def default_get(self, fields):    
        res = super(emailWizard, self).default_get(fields)
        res['sending_email_adress'] = self.getUsagerEmailAdress(self.env.context.get('default_sending_id'))
        return res
