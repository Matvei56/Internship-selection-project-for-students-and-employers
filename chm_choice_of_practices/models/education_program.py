from odoo import models, fields, api


class EducationProgram(models.Model):
    _name = 'chm_choice_of_practices.education_program'
    _description = 'Освітня програма'

    name = fields.Char(string='Назва освітньої програми', )
    degree = fields.Selection([
        ('bachelor', 'Бакалавр'),
        ('master', 'Магістр'),
        ('phd', 'Доктор філософії'),
    ], string='Освітній ступінь')

    specialty = fields.Char(string='Спеціальність', )

    status = fields.Selection([
        ('project', 'Проєкт'),
        ('approved', 'Затверджено'),
    ], string='Статус програми')

    curriculum = fields.Text(
        string='Навчальні плани'
    )

    start_date = fields.Date(
        string='Дата введення в дію'
    )

    admission_year = fields.Char(
        string='Рік набору'
    )

    stakeholder_reviews = fields.Text(
        string='Відгуки (рецензії) стейкхолдерів'
    )

    changes = fields.Text(
        string='Зміни до програми'
    )

    faculty = fields.Char(
        string='ННІ (факультет)'
    )

    department = fields.Char(
        string='Випускова кафедра'
    )


class EducationProgramLine(models.Model):
    _name = 'chm_choice_of_practices.education_program_line'

    enterprises_id = fields.Many2one(comodel_name="chm_choice_of_practices.enterprises", string="Підприємство")
    education_program_id = fields.Many2one(comodel_name="chm_choice_of_practices.education_program",
                                           string="Освітні програми")
    name = fields.Char(string='Назва освітньої програми', )
    degree = fields.Selection([
        ('bachelor', 'Бакалавр'),
        ('master', 'Магістр'),
        ('phd', 'Доктор філософії'),
    ], string='Освітній ступінь')

    specialty = fields.Char(string='Спеціальність', )

    status = fields.Selection([
        ('project', 'Проєкт'),
        ('approved', 'Затверджено'),
    ], string='Статус програми')

    curriculum = fields.Text(
        string='Навчальні плани'
    )

    start_date = fields.Date(
        string='Дата введення в дію'
    )

    admission_year = fields.Char(
        string='Рік набору'
    )

    stakeholder_reviews = fields.Text(
        string='Відгуки (рецензії) стейкхолдерів'
    )

    changes = fields.Text(
        string='Зміни до програми'
    )

    faculty = fields.Char(
        string='ННІ (факультет)'
    )

    department = fields.Char(
        string='Випускова кафедра'
    )

    @api.onchange('education_program_id')
    def _onchange_education_program(self):
        for rec in self:
            if rec.education_program_id:
                rec.name = rec.education_program_id.name
                rec.degree = rec.education_program_id.degree
                rec.specialty = rec.education_program_id.specialty
                rec.status = rec.education_program_id.status
                rec.curriculum = rec.education_program_id.curriculum
                rec.start_date = rec.education_program_id.start_date
                rec.admission_year = rec.education_program_id.admission_year
                rec.stakeholder_reviews = rec.education_program_id.stakeholder_reviews
                rec.changes = rec.education_program_id.changes
                rec.faculty = rec.education_program_id.faculty
                rec.department = rec.education_program_id.department
            else:
                rec.name = False
                rec.degree = False
                rec.specialty = False
                rec.status = False
                rec.curriculum = False
                rec.start_date = False
                rec.admission_year = False
                rec.stakeholder_reviews = False
                rec.changes = False
                rec.faculty = False
                rec.department = False
