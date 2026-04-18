from odoo import models, fields, api


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    contact_type_selection = fields.Selection(selection=[
        ('student', 'Студент'),
        ('manager', 'Керівник практики'),
        ('admin', 'Адміністратор'),
    ], string='Тип контакту', default='student')
    department_id = fields.Many2one('chm_choice_of_practices.departments',string="Кафедра", store=True)

    practice_request_ids = fields.One2many('chm_choice_of_practices.practice_request', 'student_id',
                                           string='Заяви')
    student_group_id = fields.Many2one('chm_choice_of_practices.student_group','Група')

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

    @api.model
    def create(self, vals):
        name = vals.get('name')

        if name:
            parts = name.split()

            if len(parts) == 3:
                vals['last_name'] = parts[0]
                vals['first_name'] = parts[1]
                vals['middle_name'] = parts[2]

            elif len(parts) == 2:
                vals['last_name'] = parts[0]
                vals['first_name'] = parts[1]

            elif len(parts) == 1:
                vals['first_name'] = parts[0]

        return super().create(vals)

    def write(self, vals):
        res = super().write(vals)

        if any(field in vals for field in ['first_name', 'last_name', 'middle_name']):
            self.compute_full_name()

        return res