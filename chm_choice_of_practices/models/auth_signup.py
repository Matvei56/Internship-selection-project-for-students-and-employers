from odoo import _
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
from odoo.http import request


class AuthSignupHomeInherit(AuthSignupHome):

    def _prepare_signup_values(self, qcontext):
        values = {
            key: qcontext.get(key) for key in ('login', 'password')
        }

        first_name = qcontext.get('first_name') or '1'
        last_name = qcontext.get('last_name') or ''
        middle_name = qcontext.get('middle_name') or ''

        full_name = " ".join(filter(None, [last_name, first_name, middle_name]))


        if full_name:
            values['name'] = full_name
        else:
            values['name'] = qcontext.get('login') or 'New User'

        if not values.get('password'):
            raise UserError(_("Password is required"))

        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))

        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '')
        if lang in supported_lang_codes:
            values['lang'] = lang

        return values

class AuthSignupHomeInherit(AuthSignupHome):

    @http.route()
    def web_auth_signup(self, *args, **kw):
        response = super().web_auth_signup(*args, **kw)

        groups = request.env['chm_choice_of_practices.student_group'].sudo().search([])

        response.qcontext['groups'] = groups
        return response