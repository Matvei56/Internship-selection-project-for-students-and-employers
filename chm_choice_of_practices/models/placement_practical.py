from email.policy import default
from odoo.exceptions import ValidationError
from odoo import models, fields, api


class PlacementPractical(models.Model):
    _name = 'chm_choice_of_practices.placement_practical'
    _description = 'Модель направлення на практику'

    # Назва направлення (compute)
    name = fields.Char(string="Назва", default="Нове направлення")

    state = fields.Selection([
        ('inactive', 'Неактивна'),
        ('active', 'Активна'),
        ('expired', 'Прострочена'),
    ], string="Статус")

    # Керівник практики підприємства
    head_of_practice = fields.Many2one(comodel_name="res.partner", string="Керівник практики",
                                       related="enterprises_id.partner_id")

    # Група пов'язаного студента
    students_group_id = fields.Many2one(comodel_name="chm_choice_of_practices.student_group", string="Група студенту",
                                        related="student_id.student_group_id")

    # Пов'язане підприємство
    enterprises_id = fields.Many2one(comodel_name="chm_choice_of_practices.enterprises",
                                     string="Підприємство", readonly="False")
    # Пов'язаний студент
    student_id = fields.Many2one(comodel_name="res.partner", string="Студент", required=True)

    # Активна угода підприємства
    active_practice_agreement_id = fields.Many2one('chm_choice_of_practices.practice_agreement',
                                                   string='Активна угода',
                                                   related='enterprises_id.active_practice_agreement_id')
    # Дата укладення угоди
    date_start_agreement = fields.Date(string="Дата укладення", related='active_practice_agreement_id.date_start',
                                       readonly=True, required=True)
    # Дата завершення угоди
    date_end_agreement = fields.Date(string="Дата завершення", related='active_practice_agreement_id.date_end',
                                     readonly=True)
    # Номер укладеної угоди
    number = fields.Char(string="Номер угоди", related='active_practice_agreement_id.number', readonly=False)
    # Дата початку практики
    date_start_practical = fields.Date(string="Дата початку практики",
                                       related='practice_request_id.date_from', readonly=True,  required=True)
    # Дата завершення практики
    date_end_practical = fields.Date(string="Дата завершення практики")
    # Пов'язана заява на практику
    practice_request_id = fields.Many2one('chm_choice_of_practices.practice_request', string='По\'язана заява')

    def _check_expiration(self):
        today = fields.Date.today()

        records = self.search([
            ('state', '!=', 'expired'),
            ('date_end_practical', '!=', False),
            ('date_end_practical', '<', today)
        ])

        records.write({'state': 'expired'})

    def _check_single(self):
        today = fields.Date.today()

        for rec in self:
            if rec.date_end_practical and rec.date_end_practical < today:
                rec.state = 'expired'

    @api.onchange('practice_request_id')
    def _onchange_student_id(self):
        if not self.student_id:
            self.student_id = self.practice_request_id.student_id
            self.date_end_practical = self.practice_request_id.date_to

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record._check_single()
        record.state = 'active'
        return record

    def write(self, vals):
        res = super().write(vals)
        self._check_single()
        return res

    @api.constrains('practice_request_id')
    def _check_unique_practice_request(self):
        for rec in self:
            if self.search_count([
                ('practice_request_id', '=', rec.practice_request_id.id),
                ('id', '!=', rec.id)
            ]) > 0:
                raise ValidationError(
                    "⚠️ Для цього запиту на практику вже створено направлення. "
                    "Перевірте список записів."
                )