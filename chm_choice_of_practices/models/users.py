from odoo import models, api
import logging

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model_create_multi
    def create(self, vals_list):
        users = super().create(vals_list)
        for user in users:
            user._sync_partner_contact_type()

        return users

    def write(self, vals):
        res = super().write(vals)
        for user in self:
            user._sync_partner_contact_type()

        return res

    def _sync_partner_contact_type(self):
        for user in self:
            if not user.partner_id:
                continue

            groups = user.groups_id
            if self.env.ref('chm_choice_of_practices.group_administrator') in groups:
                user.partner_id.contact_type_selection = 'admin'
            elif self.env.ref('chm_choice_of_practices.group_practice_manager') in groups:
                user.partner_id.contact_type_selection = 'manager'
            elif self.env.ref('chm_choice_of_practices.group_student') in groups:
                user.partner_id.contact_type_selection = 'student'
