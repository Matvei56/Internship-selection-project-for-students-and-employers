from odoo import models, fields, api


class PlacementPractical(models.Model):
    _name = 'chm_choice_of_practices.placement_practical'
    _description = 'Модель направлення на практику'

    # Назва направлення (compute)
    name = fields.Char(string="Назва")

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
                                       readonly=False, required=True)
    # Дата завершення угоди
    date_end_agreement = fields.Date(string="Дата завершення", related='active_practice_agreement_id.date_end',
                                     readonly=False)
    # Номер укладеної угоди
    number = fields.Char(string="Номер угоди", related='active_practice_agreement_id.number', readonly=False)
    # Дата початку практики
    date_start_practical = fields.Date(string="Дата початку практики",
                                       related='practice_request_id.date_from', readonly=False,  required=True)
    # Дата завершення практики
    date_end_practical = fields.Date(string="Дата завершення практики", related='practice_request_id.date_to',
                                     readonly=False, required=True)
    # Пов'язана заява на практику
    practice_request_id = fields.Many2one('chm_choice_of_practices.practice_request', string='По\'язана заява')
