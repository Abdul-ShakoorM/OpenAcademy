from odoo import api, fields, models


class OpenAcademy(models.Model):
    _inherit = ['res.partner']

    instructor = fields.Boolean(string='instructor', default=False)
    session_id = fields.Many2many('openacademy.session', string="Attended Sessions", readonly=True)
# class OpenAcademy(models.Model):
#     _inherit = ['res.partner']
#
#     employee_ids = fields.One2many(
#         'hr.employee', 'address_home_id', string='Employees', groups="hr.group_hr_user",
#         help="Related employees based on their private address")
#     employees_count = fields.Integer(compute='_compute_employees_count', groups="hr.group_hr_user")
