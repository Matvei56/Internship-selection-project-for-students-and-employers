from odoo import models, fields, api


class PlacementPractical(models.Model):
    _name = 'chm_choice_of_practices.placement_practical'
    _description = 'Модель направлення на практику'

    name = fields.Char(string="Назва")
