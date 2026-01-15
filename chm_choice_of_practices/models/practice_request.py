from odoo import models, fields, api


class PracticeRequest(models.Model):
    _name = 'chm_choice_of_practices.practice_request'
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
    def create(self, vals):
        record = super().create(vals)
        record.state = 'in_progress'
        return record