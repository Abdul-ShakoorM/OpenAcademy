# from odoo import models, fields, api, _
#
#
# class CreateAppointment(models.TransientModel):
#     _name = 'cancel.session'
#     _description = 'Cancel your this Session'
#     session_id = fields.Many2one('openacademy.session', string='Session Cancel')
#     partner_id = fields.Many2many('res.partner', string='Partner')
#     def action_cancel_session(self):
#         return {'type': 'ir.actions.act_window_close'} # this line of code work just for close the wizard popup
from odoo import models, fields, api


class OpenAcademy(models.TransientModel):
    _name = 'openacademy.wizard'

    def _default_sessions(self):
        return self.env['openacademy.session'].browse(self._context.get('active_id'))

    session_id = fields.Many2many('openacademy.session',
                                  string="Sessions", required=True, default=_default_sessions)
    attendee_id = fields.Many2many('res.partner', string="Attendees")

    # @api.multi
    def add_attendee(self):
        # for session in self.session_id:
        self.session_id.attendee_id |= self.attendee_id
        return {}
