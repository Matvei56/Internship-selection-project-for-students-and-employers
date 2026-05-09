from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PracticeRequest(models.Model):
    _name = 'chm_choice_of_practices.practice_request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Модель запитів на практику'

    name = fields.Char(string="Назва", required=True, default="Нова заява", compute='_compute_name')
    department_id = fields.Many2one('chm_choice_of_practices.departments', string="Кафедра", store=True)

    student_id = fields.Many2one(comodel_name="res.partner", string="Студент", required=True)
    # agreement_id = fields.Many2one(comodel_name="chm_choice_of_practices.practice_agreement", string="Угода",related="enterprises_id.agreement_id")
    enterprises_id = fields.Many2one(comodel_name="chm_choice_of_practices.enterprises", string="Підприємство")
    date_from = fields.Date(string="Дата створення", default=fields.Date.today)
    date_to = fields.Date(string="Дата завершення")
    state = fields.Selection(selection=[
        ('new', 'Нова'),
        ('in_progress', 'В обробці'),
        ('approved', 'Схвалено'),
        ('rejected', 'Відхилено'),
        ('needs_edits', 'Потребує правок'),
    ], string="Статус", default='new')
    number = fields.Char(string="Number", required=True, copy=False, readonly=True, default='New')

    comment = fields.Text(string="Коментар")
    placement_practical_ids = fields.One2many('chm_choice_of_practices.placement_practical', 'practice_request_id',
                                              string='Направлення')

    def action_approve(self):
        for record in self:
            record.state = 'approved'
        return self.action_create_direction()

    def action_reject(self):
        for record in self:
            record.state = 'rejected'

    def action_needs_edits(self):
        for record in self:
            record.state = 'needs_edits'

    def action_create_direction(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Створити направлення',
            'res_model': 'chm_choice_of_practices.placement_practical',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_enterprises_id': self.enterprises_id.id,
                'default_practice_request_id': self.id,
            }
        }

    @api.constrains('enterprises_id')
    def _check_enterprise_places(self):

        for record in self:

            if record.enterprises_id and record.enterprises_id.is_places_full:
                raise ValidationError(
                    "Неможливо створити заяву: на підприємстві вже заповнені всі місця."
                )

    @api.depends('number', 'enterprises_id', 'student_id')
    @api.onchange('number', 'enterprises_id', 'student_id')
    def _compute_name(self):
        for rec in self:
            parts = []

            if rec.number:
                parts.append(f"Заява №{rec.number}")

            if rec.student_id:
                parts.append(f"студента {rec.student_id.name}")

            if rec.enterprises_id:
                parts.append(f"про проходження практики в {rec.enterprises_id.name}")

            rec.name = " ".join(parts) if parts else "Заява"

    @api.constrains('enterprises_id')
    def _check_enterprise_active(self):
        for record in self:
            if not record.enterprises_id:
                raise ValidationError(
                    "Не можна створити запис без вибраного підприємства."
                )

            if record.enterprises_id.state != 'active':
                raise ValidationError(
                    "Неможливо створити запис, тому що угода підприємства не активована."
                )

    @api.model
    def create(self, vals_list):

        if vals_list.get('number', 'New') == 'New':
            vals_list['number'] = self.env['ir.sequence'].next_by_code(
                'chm_choice_of_practices.practice_request'
            ) or 'New'

        records = super().create(vals_list)
        records.state = 'in_progress'

        group_manager = self.env.ref('chm_choice_of_practices.group_administrator')
        managers = self.env['res.users'].search([('groups_id', 'in', [group_manager.id])])
        partners = managers.mapped('partner_id')

        for rec in records:
            student_name = rec.student_id.name
            enterprise_name = rec.enterprises_id.name

            body = (
                f"Студент <b>{student_name}</b> подав нову заявку "
                f"на підприємство <b>{enterprise_name}</b>."
            )
            rec.message_subscribe(partner_ids=partners.ids)
            rec.message_post(
                body=body,
                subject="Нова заявка на практику",
                message_type="notification",
                subtype_xmlid="mail.mt_comment",
                partner_ids=partners.ids,
                email_from="cerednikmatvei57@ukr.net",
            )

        return records
