from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class PracticeAgreement(models.Model):
    _name = 'chm_choice_of_practices.practice_agreement'
    _description = 'Угода з підприємством'
    _rec_name = 'display_name'

    number = fields.Char(string="Number", required=True, copy=False, readonly=True, default='New' )
    date_start = fields.Date(string="Дата укладення", required=True, default=fields.Date.context_today)
    state = fields.Selection([
        ('inactive', 'Неактивна'),
        ('active', 'Активована'),
        ('expired', 'Прострочена'),
    ], string="Статус", )

    is_unlimited = fields.Boolean(
        string="Безстрокова угода",
        help="Якщо відмічено, термін дії не обмежений"
    )
    is_auto_prolongation = fields.Boolean(
        string="Автоматична пролонгація",
        help="Якщо відмічено, угода автоматично продовжується, якщо не розірвана"
    )

    date_end = fields.Date(string="Термін дії до")

    enterprises_id = fields.Many2one(
        comodel_name="chm_choice_of_practices.enterprises",
        string="Підприємство", required=True, )

    practice_type = fields.Selection([
        ('educational', 'Навчальна'),
        ('industrial', 'Виробнича'),
        ('pre_diploma', 'Переддипломна'),
    ], string="Тип практики")

    season = fields.Selection([
        ('spring', 'Весна'),
        ('summer', 'Літо'),
        ('autumn', 'Осінь'),
        ('winter', 'Зима'),
    ], string="Сезонність")

    places_limit = fields.Integer(string="Ліміт місць")
    additional_conditions = fields.Text(string="Додаткові умови")

    display_name = fields.Char(compute="_compute_display_name", string='Назва', store=True)

    def action_activate(self):
        for rec in self:
            rec._check_and_update_state(raise_error=True)
            rec.state = 'active'

    def action_deactivate(self):
        for rec in self:
            rec.state = 'inactive'

    def cron_check_agreements_state(self):
        agreements = self.search([])
        agreements._check_and_update_state()

    @api.depends('number', 'enterprises_id')
    @api.onchange('number', 'enterprises_id')
    def _compute_display_name(self):
        for rec in self:
            if rec.number and rec.enterprises_id:
                rec.display_name = f"Угода №{rec.number} – {rec.enterprises_id.name}"
            else:
                rec.display_name = rec.number or "Угода"

    @api.onchange('date_start', 'date_end')
    def _check_and_update_state(self, raise_error=False):
        today = fields.Date.context_today(self)

        for rec in self:
            errors = []

            if rec.date_end and rec.date_end < rec.date_start:
                errors.append("Дата завершення не може бути раніше дати початку.")

            if not rec.is_unlimited and not rec.is_auto_prolongation:
                if rec.date_end and rec.date_end < today:
                    errors.append("Термін дії угоди вже закінчився.")

            if not rec.is_unlimited and not rec.is_auto_prolongation and not rec.date_end:
                errors.append("Потрібно вказати дату завершення або зробити угоду безстроковою.")

            if errors:
                rec.state = 'inactive'
                if raise_error:
                    raise ValidationError("\n".join(errors))
                continue

            if rec.date_end and rec.date_end < today:
                rec.state = 'expired'
            else:
                rec.state = 'active'

    @api.constrains('state', 'enterprises_id')
    def _check_only_one_active_agreement(self):
        for record in self:
            if record.state == 'active' and record.enterprises_id:
                active_count = self.search_count([
                    ('enterprises_id', '=', record.enterprises_id.id),
                    ('state', '=', 'active'),
                    ('id', '!=', record.id),
                ])
                if active_count > 0:
                    raise ValidationError(
                        'У підприємства може бути тільки одна активна угода!'
                    )

    @api.model
    def create(self, vals):

        if vals.get('number', 'New') == 'New':
            vals['number'] = self.env['ir.sequence'].next_by_code(
                'chm_choice_of_practices.practice_agreement'
            ) or 'New'

        record = super().create(vals)
        record.state = 'active'
        record._check_and_update_state()

        return record

    def write(self, vals):
        res = super().write(vals)

        if 'state' in vals:
            for rec in self:
                if rec.enterprises_id:
                    rec.enterprises_id._check_and_update_state_from_agreements()

        return res
