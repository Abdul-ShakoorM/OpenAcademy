# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import ValidationError
# for calender view
from datetime import timedelta


class OpenAcademy(models.Model):
    _name = 'openacademy.session'
    _description = 'openacademy provide different session'
    _rec_name = 'instructor'

    name = fields.Char(string='Title', required=True)
    start_date = fields.Date(string="Dated", default=date.today())
    # duration = fields.Char('Duration')
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    no_of_seats = fields.Integer('No of Seats')
    active = fields.Boolean(default=True)
    # active = fields.Boolean(default=True)
    color = fields.Integer()
    # 1st time
    # instructor = fields.Many2one('res.partner', 'Instructor', ) # Many2One(''model.name' , 'string' )
    # then modifify according exercise domain
    # instructor = fields.Many2one('res.partner', string="Instructor",
    #                                 domain=[('instructor', '=', True)])
    # after this only add complix domains
    instructor = fields.Many2one('res.partner', string="Instructor",
                                 domain=['|', ('instructor', '=', True),
                                         ('category_id.name', 'ilike', "Teacher")])
    course_id = fields.Many2one('openacademy.course', 'Course')
    attendee_id = fields.Many2many('res.partner', string="Attendees")

    # for adding parsentage in takan seat   //Dependencies//
    taken_no_of_seats = fields.Float(string="Taken Seats", compute='_taken_no_of_seats')
    # calendar view
    end_date = fields.Date(string="End Date", store=True,
                           compute='_get_end_date', inverse='_set_end_date')
    # gantt view
    hours = fields.Float(string="Duration in hours",
                         compute='_get_hours', inverse='_set_hours')
    attendees_count = fields.Integer(
        string="Attendees count", compute='_get_attendees_count', store=True)

    @api.depends('no_of_seats', 'attendee_id')
    def _taken_no_of_seats(self):
        for r in self:
            if not r.no_of_seats:
                r.taken_no_of_seats = 0.0
            else:
                r.taken_no_of_seats = 100.0 * len(r.attendee_id) / r.no_of_seats

    # OnChang work....
    @api.onchange('no_of_seats', 'attendee_id')
    def _verify_valid_seats(self):
        if self.no_of_seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'Number of seats' value",
                    'message': "The number of available seats may not be negative",
                },
            }
        if self.no_of_seats < len(self.attendee_id):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase No. Of seats or remove excess attendees",
                },
            }
        # calendar memoryview

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            # Add duration to start_date, but: Monday + 5 days barabr Saturday
            # subtract one second to get on Friday instead
            start = fields.Datetime.from_string(r.start_date)
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = start + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue

            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            start_date = fields.Datetime.from_string(r.start_date)
            end_date = fields.Datetime.from_string(r.end_date)
            r.duration = (end_date - start_date).days + 1
            # end calendar view

    # gant view
    @api.depends('duration')
    def _get_hours(self):
        for r in self:
            r.hours = r.duration * 24

    def _set_hours(self):
        for r in self:
            r.duration = r.hours / 24
            # end
            # graph
    @api.depends('attendee_id')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_id)
                    # end
    @api.constrains('instructor', 'attendee_id')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor and r.instructor in r.attendee_id:
                raise ValidationError("A session's instructor can't be an attendee")