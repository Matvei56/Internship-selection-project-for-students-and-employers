from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PracticeRequest(models.Model):
    _name = 'chm_choice_of_practices.practice_request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Модель запитів на практику'

    name = fields.Char(string="Назва", required=True, default="Нова заява")
    student_id = fields.Many2one(comodel_name="res.partner", string="Студент", required=True)
    agreement_id = fields.Many2one(comodel_name="chm_choice_of_practices.practice_agreement", string="Угода")
    enterprises_id = fields.Many2one(comodel_name="chm_choice_of_practices.enterprises", string="Підприємство")
    date_from = fields.Date(string="Дата створення", default=fields.Date.today)
    date_to = fields.Date(string="Дата завершення")
    state = fields.Selection(selection=[
        ('new', 'Нова'),
        ('in_progress', 'В обробці'),
        ('approved', 'Схвалено'),
        ('rejected', 'Відхилено'),
        ('needs_edits', 'Потребує правок'),
    ], string="Статус", default='new')
    comment = fields.Text(string="Коментар")

    def action_approve(self):
        for record in self:
            record.state = 'approved'

    def action_reject(self):
        for record in self:
            record.state = 'rejected'

    def action_needs_edits(self):
        for record in self:
            record.state = 'needs_edits'


    @api.model
    def create(self, vals_list):
        records = super().create(vals_list)
        records.state = 'in_progress'

        group_manager = self.env.ref('chm_choice_of_practices.group_practice_manager')
        managers = self.env['res.users'].search([('groups_id', 'in', [group_manager.id])])
        partners = managers.mapped('partner_id')

        for rec in records:
            student_name = rec.student_id.name
            enterprise_name = rec.enterprises_id.name

            body = (
                f"Студент <b>{student_name}</b> подав нову заявку "
                f"на підприємство <b>{enterprise_name}</b>."
            )

            rec.message_subscribe(partner_ids=partners.ids)
            rec.message_post(
                body=body,
                subject="Нова заявка на практику",
                message_type="comment",
            )

            for partner in partners:
                partner.message_notify(
                    body=body,
                    subject="Нова заявка на практику"
                )

        return records

