from odoo import models, fields, api


class Departments(models.Model):
    _name = 'chm_choice_of_practices.departments'
    _description = 'Модель кафедр'

    name = fields.Char(string="Назва")
    institutes_id = fields.Many2one('chm_choice_of_practices.institutes', string="Інститут")
