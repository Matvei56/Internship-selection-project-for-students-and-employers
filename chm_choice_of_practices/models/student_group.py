from odoo import models, fields, api
from datetime import date


class StudentGroup(models.Model):
    _name = 'chm_choice_of_practices.student_group'
    _description = 'Модель груп студентів'

    name = fields.Char(string="Назва", compute="_compute_name", store=True)
    abbreviation = fields.Char(string="Абревіатура", required=True)
    number = fields.Char(string="Номер", required=True)
    full_name = fields.Char(string="Повна назва", readonly=True)
    education_program_program_id = fields.Many2one(comodel_name='chm_choice_of_practices.education_program',
                                                   string="Освітня програма")
    course = fields.Integer(string="Курс", compute="_compute_course", store=True)

    @api.depends('number')
    def _compute_course(self):

        today = date.today()
        if today.month >= 9:
            academic_year = today.year
        else:
            academic_year = today.year - 1

        for rec in self:
            rec.course = 0

            if rec.number and len(rec.number) >= 2:
                try:
                    year_short = int(rec.number[:2])
                    year_start = 2000 + year_short

                    rec.course = academic_year - year_start + 1

                except ValueError:
                    rec.course = 0

    def recompute_courses_cron(self):
        records = self.search([])
        records._compute_course()

    @api.depends('abbreviation', 'number')
    @api.onchange('abbreviation', 'number')
    def _compute_name(self):
        for rec in self:
            if rec.abbreviation and rec.number:
                rec.name = f"{rec.abbreviation} - {rec.number}"
            else:
                rec.name = False
