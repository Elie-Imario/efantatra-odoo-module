# -*- coding: utf-8 -*-
import os
from twilio.rest import Client
from odoo import api, fields, models

class smsWizard(models.TransientModel):
    _name='efantatra.sms.wizard'
    _description='efantatra_sms_wizard'

    message = fields.Text("Message")
    usager_id = fields.Integer("Id_Usager")
    usager_name = fields.Char("Nom Usager")

    def getUsagerPhone(self, _id):
        self.env.cr.execute(f"SELECT phone_number FROM efantatra_usage WHERE id={_id}")
        try:
            _phone_number = int(self.env.cr.fetchone()[0])
        except Exception as e:
            _phone_number = None

        return _phone_number
    
    def getUsagerName(self, _id):
        self.env.cr.execute(f"SELECT name_usager FROM efantatra_usage WHERE id={_id}")
        try:
            _name_usager = self.env.cr.fetchone()[0]
        except Exception as e:
            _name_usager = None

        return _name_usager

    def _send_sms_with_api(self, _mobile, _message):
        account_sid = 'ACc36f1fff1db9f906bfe3773e81aa09cc'
        auth_token = 'a387d0fa791e50d96c30f602be5e5b3a'
        client = Client(account_sid, auth_token)

        message = client.messages \
                        .create(
                            body=_message,
                            from_='+19036238512',
                            to='+261326790460'
                        )

        print(message.sid)

    def sendSMS(self):
        try:
            self._send_sms_with_api(self.getUsagerPhone(self.usager_id), self.message)
        except Exception as e:
            print("Error\n")


    @api.model
    def default_get(self, fields):    
        res = super(smsWizard, self).default_get(fields)
        res['usager_name'] = self.getUsagerName(self.env.context.get('default_usager_id'))
        return res