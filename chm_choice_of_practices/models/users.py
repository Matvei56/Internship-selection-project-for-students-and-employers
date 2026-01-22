from odoo import models, api
import logging

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model_create_multi
    def create(self, vals_list):
        users = super().create(vals_list)
        for user in users:
            user._sync_partner_contact_type()
            user._sync_student_only_group()
        return users

    def write(self, vals):
        res = super().write(vals)
        for user in self:
            user._sync_partner_contact_type()
            user._sync_student_only_group()
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
            else:
                user.partner_id.contact_type_selection = False

    def _sync_student_only_group(self):
        group_student = self.env.ref('chm_choice_of_practices.group_student')
        group_student_only = self.env.ref('chm_choice_of_practices.group_student_only')
        group_admin = self.env.ref('chm_choice_of_practices.group_administrator')

        for user in self:
            has_student = group_student in user.groups_id
            has_admin = group_admin in user.groups_id
            has_student_only = group_student_only in user.groups_id

            if has_student and not has_admin and not has_student_only:
                user.write({
                    'groups_id': [(4, group_student_only.id)]
                })

            elif (not has_student or has_admin) and has_student_only:
                user.write({
                    'groups_id': [(3, group_student_only.id)]
                })
