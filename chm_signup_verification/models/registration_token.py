from odoo import models, fields, api
import uuid
from datetime import datetime, timedelta

class RegistrationToken(models.Model):
    _name = 'chm.registration.token'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Token for Email Verification'

    email = fields.Char(required=True, index=True)
    token = fields.Char(required=True, default=lambda self: str(uuid.uuid4()))
    is_used = fields.Boolean(default=False)
    expiry_date = fields.Datetime(default=lambda self: fields.Datetime.now() + timedelta(hours=24))

    def send_verification_email(self):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        verify_url = f"{base_url}/signup/verify/{self.token}"

        body = f"""
                <div style="margin: 0px; padding: 30px; font-family: Arial, sans-serif;">
                    <h2>Вітаємо!</h2>
                    <p>Ви почали процес реєстрації. Щоб підтвердити свою пошту, натисніть на кнопку нижче:</p>
                    <div style="margin: 35px 0;">
                        <a href="{verify_url}" 
                           style="background-color: #875A7B; padding: 12px 25px; text-decoration: none; color: white; border-radius: 5px; font-weight: bold;">
                            Підтвердити Email
                        </a>
                    </div>
                    <p>Або перейдіть за посиланням: {verify_url}</p>
                </div>
            """

        mail_values = {
            'subject': "Підтвердження реєстрації",
            'body_html': body,
            'email_to': self.email,
            'email_from': "cerednikmatvei57@ukr.net",
        }

        mail = self.env['mail.mail'].sudo().create(mail_values)
        mail.send()
