from odoo import models, fields, api


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    contact_type_selection = fields.Selection(selection=[
        ('student', 'Студент'),
        ('manager', 'Керівник практики'),
        ('admin', 'Адміністратор'),
    ], string='Тип контакту', default='student')

    student_group = fields.Many2one('chm_choice_of_practices.student_group','Група')
    practice_request_ids = fields.One2many('chm_choice_of_practices.practice_request', 'student_id',
                                           string='Заяви')
    first_name = fields.Char(string="Ім'я")
    last_name = fields.Char(string="Прізвище")
    middle_name = fields.Char(string="По батькові")

    # full_name = fields.Char(
    #     string="ПІБ",
    #     compute="_compute_full_name",
    #     store=True
    # )

    @api.depends('first_name', 'last_name', 'middle_name')
    @api.onchange('first_name', 'last_name', 'middle_name')
    def compute_full_name(self):
        for rec in self:
            parts = [
                rec.last_name or '',
                rec.first_name or '',
                rec.middle_name or ''
            ]
            rec.name = " ".join(p for p in parts if p)
