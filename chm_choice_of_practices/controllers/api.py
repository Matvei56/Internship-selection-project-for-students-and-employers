import odoo
from odoo import http, api, SUPERUSER_ID
from odoo.http import request
import json


class EnterprisesController(http.Controller):

    @http.route('/api/v1/enterprises', type='http', auth='none', methods=['GET'], csrf=False)
    def get_enterprises(self, db='odoo6', **kwargs):
        api_key = request.httprequest.headers.get('API-Key')
        if not api_key:
            return self._send_json({'error': 'No API Key provided'}, status='401 Unauthorized')

        try:
            registry = odoo.registry(db)
            with registry.cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, {})
                api_key_owners = env['res.users.apikeys'].search([]).mapped('user_id')

                target_uid = False
                for user in api_key_owners:
                    try:
                        uid = env['res.users'].authenticate(db, user.login, api_key, {'interactive': False})
                        if uid:
                            target_uid = uid
                            break
                    except Exception:
                        continue

                if not target_uid:
                    return self._send_json({'error': 'Invalid API Key or Login not found'}, status='401 Unauthorized')

                user_env = api.Environment(cr, target_uid, {})
                enterprises = user_env['chm_choice_of_practices.enterprises'].search([])

                result = []
                for ent in enterprises:
                    requests_list = []
                    for req in ent.practice_request_ids:
                        requests_list.append({
                            'id': req.id,
                            'name': req.name,

                        })

                    result.append({
                        'id': ent.id,
                        'name': ent.name,
                        'partner_id': ent.partner_id.name,
                        'practice_type': ent.practice_type,
                        'edrpou': ent.edrpou,
                        'state': ent.state,
                        'active_practice_agreement_id': ent.active_practice_agreement_id.number,

                        'practice_requests': requests_list
                    })
                return self._send_json(result)

        except Exception as e:
            return self._send_json({'error': 'Server Error', 'details': str(e)}, status='500 Internal Server Error')

    def _send_json(self, data, status='200 OK'):
        response = request.make_response(
            json.dumps(data, ensure_ascii=False),
            headers=[('Content-Type', 'application/json')]
        )
        response.status = status
        return response