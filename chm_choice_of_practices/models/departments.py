from odoo import models, fields, api


class Departments(models.Model):
    _name = 'chm_choice_of_practices.departments'
    _description = 'Модель кафедр'

    # Назва кафедри
    name = fields.Char(string="Назва")

    # Підв'язка до інституту
    institutes_id = fields.Many2one('chm_choice_of_practices.institutes', string="Інститут")
    education_program_ids = fields.One2many('chm_choice_of_practices.education_program', 'departments_id')
