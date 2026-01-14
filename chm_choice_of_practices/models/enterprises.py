from odoo import models, fields, api


class Enterprises(models.Model):
    _name = 'chm_choice_of_practices.enterprises'
    _description = 'Модель підприємств'

    name = fields.Char(string="Назва", required=True)
    partner_id = fields.Many2one('res.partner', 'Особа' )
    edrpou = fields.Char(string="ЄДРПОУ")
    address = fields.Char(string="Адреса")
    cite = fields.Char(string="Сайт")
    field_of_activity = fields.Char(string="Сфера діяльності")
    notes = fields.Text(string="Примітки")
