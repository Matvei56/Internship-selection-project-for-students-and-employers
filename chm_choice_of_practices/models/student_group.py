from odoo import models, fields, api


class StudentGroup(models.Model):
    _name = 'chm_choice_of_practices.student_group'
    _description = 'Модель груп студентів'

    name = fields.Char(string="Назва", compute="_compute_name", store=True)
    abbreviation = fields.Char(string="Абревіатура")
    number = fields.Char(string="Номер")
    full_name = fields.Char(string="Повна назва")

    @api.depends('abbreviation', 'number')
    @api.onchange('abbreviation', 'number')
    def _compute_name(self):
        for rec in self:
            if rec.abbreviation and rec.number:
                rec.name = f"{rec.abbreviation} - {rec.number}"
            else:
                rec.name = False
