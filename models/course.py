# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpenAcademy(models.Model):
    _name = 'openacademy.course'
    _description = 'openacademy course are best'

    name = fields.Char('Name')
    description = fields.Text('Description')
    title = fields.Char('Title', readonly=True,
                        default=lambda self: _('New'))
    responsible_user = fields.Many2one('res.users', 'Responsible User')
    session_id = fields.One2many('openacademy.session', 'course_id', string="Session")


    # @api.multi
    # def copy(self, default=None):
    #     default = dict(default or {})
    #
    #     copied_count = self.search_count(
    #         [('name', '=like', u"Copy of {}%".format(self.name))])
    #     if not copied_count:
    #         new_name = u"Copy of {}".format(self.name)
    #     else:
    #         new_name = u"Copy of {} ({})".format(self.name, copied_count)
    #
    #     default['name'] = new_name
    #     return super(Course, self).copy(default)

    # relivant to session_id. for uniq session title & discription... sql constrainst hai ya. python constraint  session main hai attend py
    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]
    # Status bar states
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done')
    ], string="Status", default='draft', tracking=True)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'
    def unlink(self):
        if self.state == 'done':
            raise ValidationError(f"You can't delete {self.reference} as it is in done state")
        rec = super(OpenAcademy, self).unlink()
        return rec


    @api.model
    def create(self, values):
        if values.get('title', _('New')) == _('New'):
            values['title'] = self.env['ir.sequence'].next_by_code('openacademy.course') or _('New')
        return super(OpenAcademy, self).create(values)