from odoo import models, fields, api


class PracticeAgreement(models.Model):
    _name = 'chm_choice_of_practices.practice_agreement'
    _description = 'Модель угод про практику'

    name = fields.Char(string="Назва", required=True)
