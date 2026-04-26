from odoo import models
from odoo.exceptions import AccessError

class XlsxReportPatch(models.Model):
    _inherit = 'ir.actions.report'

    # Функція стопор щоб надрукувати звіт міг тільки адмін
    def _render_xlsx_jinja_mode(self, template_path, doc_obj, data, context, report_name="report"):
        if not self.env.user.has_group('chm_choice_of_practices.group_administrator'):
            raise AccessError("Ви не маєте права на друк цього звіту")
        return super()._render_xlsx_jinja_mode(template_path, doc_obj, data, context, report_name)
