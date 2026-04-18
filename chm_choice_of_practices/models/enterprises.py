from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Enterprises(models.Model):
    _name = 'chm_choice_of_practices.enterprises'
    _description = 'Модель підприємств'

    name = fields.Char(string="Назва", required=True)
    partner_id = fields.Many2one('res.partner', 'Відповідальна особа', default=lambda self: self.env.user.partner_id)
    practice_type = fields.Selection([
        ('educational', 'Навчальна'),
        ('project_technological', 'Проєктно-технологічна'),
        ('industrial', 'Виробнича'),
        ('pre_diploma', 'Переддипломна'),
    ], string="Тип практики")
    edrpou = fields.Char(string="ЄДРПОУ")
    address = fields.Char(string="Адреса")
    cite = fields.Char(string="Сайт")
    field_of_activity = fields.Char(string="Сфера діяльності")
    notes = fields.Text(string="Примітки")
    state = fields.Selection([
        ('inactive', 'Угода не активована'),
        ('active', 'Угода активована'),
    ], string="Статус угоди")
    practice_request_ids = fields.One2many('chm_choice_of_practices.practice_request', 'enterprises_id',
                                           string='Заяви')

    practice_agreement_ids = fields.One2many('chm_choice_of_practices.practice_agreement', 'enterprises_id',
                                             string='Угоди')
    active_practice_agreement_id = fields.Many2one(
        'chm_choice_of_practices.practice_agreement',
        string='Активна угода',
        compute='_compute_active_practice_agreement',
        store=True
    )
    practice_request_count = fields.Integer(
        string='Усьго заяв до підприємства', compute='_compute_practice_request_count', store=False)
    enterprises_count = fields.Integer(
        string='Усьго підприємств', compute='_compute_enterprises_count', store=False)

    new_request_count = fields.Integer(compute="_compute_practice_request_counts", string="Нові")
    in_progress_request_count = fields.Integer(compute="_compute_practice_request_counts", string="В обробці")
    approved_request_count = fields.Integer(compute="_compute_practice_request_counts", string="Схвалені")
    rejected_request_count = fields.Integer(compute="_compute_practice_request_counts", string="Відхилені")
    needs_edits_request_count = fields.Integer(compute="_compute_practice_request_counts", string="Потребують правок")
    education_program_count = fields.Integer(compute="_compute_education_program_count", string="Освітні програми")

    enterprises_ids = fields.Many2many(
        'chm_choice_of_practices.enterprises',
        compute='_compute_enterprises_ids',
        string='Всі підприємства',
        store=False,
        readonly=True
    )

    current_user_id = fields.Many2one(
        'res.users',
        string="Поточний юзер",
        compute="_compute_current_user",
        store=False
    )
    education_program_line_ids = fields.One2many('chm_choice_of_practices.education_program_line', 'enterprises_id',
                                            string='Освітні програми')

    @api.depends('practice_agreement_ids.state')
    def _compute_active_practice_agreement(self):
        for record in self:
            active = record.practice_agreement_ids.filtered(
                lambda r: r.state == 'active'
            )
            record.active_practice_agreement_id = active[:1].id if active else False

    @api.depends('practice_request_ids')
    def _compute_practice_request_counts(self):
        for rec in self:
            new = in_progress = approved = rejected = needs_edits = 0

            for req in rec.practice_request_ids:
                if req.state == 'new':
                    new += 1
                elif req.state == 'in_progress':
                    in_progress += 1
                elif req.state == 'approved':
                    approved += 1
                elif req.state == 'rejected':
                    rejected += 1
                elif req.state == 'needs_edits':
                    needs_edits += 1

            rec.new_request_count = new
            rec.in_progress_request_count = in_progress
            rec.approved_request_count = approved
            rec.rejected_request_count = rejected
            rec.needs_edits_request_count = needs_edits
            rec.practice_request_count = len(rec.practice_request_ids)

    @api.depends()
    def _compute_current_user(self):
        for rec in self:
            rec.current_user_id = self.env.user

    @api.depends('practice_request_ids')
    def _compute_practice_request_count(self):
        for record in self:
            record.practice_request_count = len(record.practice_request_ids)

    @api.depends('education_program_line_ids')
    def _compute_education_program_count(self):
        for record in self:
            record.education_program_count = len(record.education_program_line_ids)

    @api.depends('enterprises_ids')
    def _compute_enterprises_count(self):
        for record in self:
            record.enterprises_count = len(record.enterprises_ids)

    @api.depends('enterprises_ids')
    def _compute_enterprises_ids(self):
        all_enterprises = self.env['chm_choice_of_practices.enterprises'].search([])
        for rec in self:
            rec.enterprises_ids = all_enterprises

    def actions_create_request(self):
        if self.state != 'active':
            raise ValidationError('Не можна створити заявку: підприємство не активне!')

        return {
            'type': 'ir.actions.act_window',
            'name': 'Перевірка даних',
            'res_model': 'partner.check.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_partner_id': self.env.user.partner_id.id,
                'default_enterprises_id': self.id,
            }
        }

    @api.onchange('practice_agreement_ids')
    @api.depends('practice_agreement_ids')
    def _check_and_update_state_from_agreements(self):
        for rec in self:
            active_exists = any(
                agreement.state == 'active'
                for agreement in rec.practice_agreement_ids
            )

            rec.state = 'active' if active_exists else 'inactive'

    @api.constrains('enterprises_id')
    def _check_enterprise_active(self):
        for record in self:
            if record.enterprises_id and record.enterprises_id.state != 'active':
                raise ValidationError(
                    'Не можна створити заявку: підприємство не активне!'
                )

    @api.model
    def create(self, vals):
        record = super().create(vals)

        all_enterprises = self.env['chm_choice_of_practices.enterprises'].search([])
        record.enterprises_ids = [(6, 0, all_enterprises.ids)]

        enterprise = self.env['chm_choice_of_practices.enterprises'].browse(
            vals.get('enterprises_id')
        )

        if enterprise and enterprise.state != 'active':
            raise ValidationError(
                'Не можна створити заявку: підприємство не активне!'
            )
        return record
