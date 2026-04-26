from odoo import http, fields
from odoo.http import request


class SignupVerifyController(http.Controller):


    @http.route('/signup/email_input', type='http', auth='public', website=True)
    def signup_email_input(self, **kw):
        return request.render('chm_signup_verification.email_input_template')


    @http.route('/signup/send_token', type='http', auth='public', methods=['POST'], website=True, csrf=True)
    def send_token(self, email, **kw):

        user_exists = request.env['res.users'].sudo().search([('login', '=', email)])
        if user_exists:
            return request.render('chm_signup_verification.email_input_template',
                                  {'error': 'This email address has already been registered'})


        token_rec = request.env['chm.registration.token'].sudo().create({'email': email})
        token_rec.send_verification_email()

        return request.render('chm_signup_verification.check_email_message')


    @http.route('/signup/verify/<string:token>', type='http', auth='public', website=True)
    def verify_token(self, token, **kw):
        token_rec = request.env['chm.registration.token'].sudo().search([
            ('token', '=', token),
            ('is_used', '=', False),
            ('expiry_date', '>', fields.Datetime.now())
        ], limit=1)

        if not token_rec:
            return "<h3>Error: The link is invalid or has expired.</h3>"


        token_rec.is_used = True

        return request.redirect('/web/signup?login=%s' % token_rec.email)