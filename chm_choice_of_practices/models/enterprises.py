from odoo import models, fields, api


class Enterprises(models.Model):
    _name = 'chm_choice_of_practices.enterprises'
    _description = 'Модель підприємств'

    name = fields.Char(string="Назва", required=True)
    partner_id = fields.Many2one('res.partner', 'Особа')
    edrpou = fields.Char(string="ЄДРПОУ")
    address = fields.Char(string="Адреса")
    cite = fields.Char(string="Сайт")
    field_of_activity = fields.Char(string="Сфера діяльності")
    notes = fields.Text(string="Примітки")
    state = fields.Selection([
        ('inactive', 'Угода не активна'),
        ('active', 'Угода активна'),
    ], string="Статус угоди", tracking=True)

    practice_request_ids = fields.One2many('chm_choice_of_practices.practice_request', 'enterprises_id',
                                           string='Заяви')

    practice_agreement_ids = fields.One2many('chm_choice_of_practices.practice_agreement', 'enterprises_id',
                                           string='Угоди')

    def actions_create_request(self):
        self.env.user.notify_info(message='Створення заяви', title='Службове повідомлення')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Створити заяву',
            'res_model': 'chm_choice_of_practices.practice_request',
            'view_mode': 'form',
            'view_id': self.env.ref('chm_choice_of_practices.view_form_practice_request').id,
            'target': 'current',
            'context': {
                'default_state': 'new',
                'default_student_id': self.env.user.partner_id.id,
                'default_enterprises_id': self.id,
            },
        }

    @api.onchange('practice_agreement_ids')
    @api.depends('practice_agreement_ids')
    def _check_and_update_state_from_agreements(self):
        for rec in self:
            active_exists = any(
                agreement.state == 'active'
                for agreement in rec.practice_agreement_ids
            )

            rec.state = 'active' if active_exists else 'inactive'