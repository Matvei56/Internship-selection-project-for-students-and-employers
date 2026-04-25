from . import models
from . import wizard
from . import controllers
from odoo import api, SUPERUSER_ID
from odoo.exceptions import AccessError


def post_init_hook(cr, registry):
    from odoo.api import Environment
    env = api.Environment(cr, SUPERUSER_ID, {})


