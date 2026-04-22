from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Institutes(models.Model):
    _name = 'chm_choice_of_practices.institutes'

    name = fields.Char(string="Назва")
    departments_ids = fields.One2many('chm_choice_of_practices.departments', 'institutes_id',
                                             string='Кафедри')
