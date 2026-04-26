from odoo import models, fields, api


class PartnerCheckWizard(models.TransientModel):
    _name = 'partner.check.wizard'
    _description = 'Перевірка даних партнера'

    partner_id = fields.Many2one('res.partner')
    enterprises_id = fields.Many2one(comodel_name="chm_choice_of_practices.enterprises", string="Підприємство")
    student_group_id = fields.Many2one('chm_choice_of_practices.student_group','Група')

    first_name = fields.Char(string="Ім'я",  readonly=False)
    last_name = fields.Char(string="Прізвище", readonly=False)
    middle_name = fields.Char(string="По батькові", readonly=False)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        partner = self.env.user.partner_id

        res.update({
            'partner_id': partner.id,
            'first_name': partner.first_name,
            'last_name': partner.last_name,
            'middle_name': partner.middle_name,
            'student_group_id': partner.student_group_id,
        })

        return res

    def action_confirm(self):
        self.partner_id.write({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'student_group_id': self.student_group_id,
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Створити заяву',
            'res_model': 'chm_choice_of_practices.practice_request',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_state': 'new',
                'default_student_id': self.partner_id.id,
                'default_enterprises_id': self.enterprises_id.id,
                'default_student_group_id': self.student_group_id.id,
            },
        }