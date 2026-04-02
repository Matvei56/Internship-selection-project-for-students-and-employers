from odoo import models, fields, api


class PlacementPractical(models.Model):
    _name = 'chm_choice_of_practices.placement_practical'
    _description = 'Модель направлення на практику'

    name = fields.Char(string="Назва")
    head_of_practice = fields.Many2one(comodel_name="res.partner", string="Керівник практики",
                                       related="enterprises_id.partner_id")
    enterprises_id = fields.Many2one(comodel_name="chm_choice_of_practices.enterprises",
                                     string="Підприємство", readonly="True")
    active_practice_agreement_id = fields.Many2one(
        'chm_choice_of_practices.practice_agreement',
        string='Активна угода',
        related='enterprises_id.active_practice_agreement_id')
    date_start_agreement = fields.Date(string="Дата укладення", related='active_practice_agreement_id.date_start')
    number = fields.Char(string="Номер угоди", related='active_practice_agreement_id.number')

