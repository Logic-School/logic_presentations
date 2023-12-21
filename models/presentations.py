from odoo import fields, models, api


class LogicPresentation(models.Model):
    _name = "logic.presentations"
    _description = "Presentation"
    name = fields.Char(string="Name", compute="_compute_name")

    def _compute_name(self):
        for record in self:
            if record.batch_id and record.date:
                record.name = str(record.date) + " - " + str(record.batch_id.name)
            else:
                record.name = False

    coordinator = fields.Many2one('res.users', string="Coordinator", readonly=True, default=lambda self: self.env.user)
    batch_id = fields.Many2one('logic.base.batch', string="Batch", required=True)
    date = fields.Date(string="Date", required=True)
    branch = fields.Many2one('logic.base.branches', related='batch_id.branch_id', string="Branch")
    student_presentations = fields.One2many('logic.student.presentation', 'presentation_id', string='Presentations')
    total_students = fields.Integer(string="Total Strength", compute="get_total_students", readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('submit', 'Submitted')], default='draft', string="State",
                             tracking=True)
    course_id = fields.Many2one('logic.base.courses', string="Course", related='batch_id.course_id')
    faculty_id = fields.Many2one('res.users', string="Faculty", domain=[('faculty_check', '=', True)],)

    def action_submit(self):
        students = self.env['logic.students'].sudo().search([])
        for student in students:
            for record in self.student_presentations:
                if record.student_id.id == student.id:
                    print(student.name, 'student')
                    student.presentation_date = self.date
                    student.presentation_rating = record.rating
                    student.presentation_feedback = record.feedback
        self.state = 'submit'

    @api.depends('batch_id')
    def get_total_students(self):
        for record in self:
            if record.batch_id:
                record.total_students = self.env['logic.students'].search_count([('batch_id', '=', record.batch_id.id)])
            else:
                record.total_students = 0

    presentation_count = fields.Integer(string="Students Presented", compute="_compute_presentation_count")

    def _compute_presentation_count(self):
        for record in self:
            record.presentation_count = len(record.student_presentations)


class StudentPresentation(models.Model):
    _name = "logic.student.presentation"
    student_id = fields.Many2one('logic.students', string="Student", required=True)
    presentation_id = fields.Many2one('logic.presentations', string="Presentation")
    feedback = fields.Text(string="Feedback")
    rating = fields.Selection(
        selection=[('0', 'No rating'), ('1', 'Very Poor'), ('2', 'Poor'), ('3', 'Average'), ('4', 'Good'),
                   ('5', 'Very Good')], string="Rating", default='0')
    batch_id = fields.Many2one('logic.base.batch', string="Batch")

    @api.onchange('batch_id')
    def get_students_domain(self):
        already_presented_stud_ids = []
        for presentation in self.presentation_id.student_presentations:
            already_presented_stud_ids.append(presentation.student_id.id)
        return {'domain': {
            'student_id': [('batch_id', '=', self.batch_id.id), ('id', 'not in', already_presented_stud_ids)]}}


