from odoo import fields,models,api

class LogicPresentation(models.Model):
    _name="logic.presentations"
    _description="Presentation"
    name = fields.Char(string="Name",compute="_compute_name")
    def _compute_name(self):
        for record in self:
            if record.batch_id and record.date:
                record.name = str(record.date) + " - " + str(record.batch_id.name)
            else:
                record.name = False
    coordinator = fields.Many2one('res.users',string="Coordinator",readonly=True,default=lambda self: self.env.user)
    batch_id = fields.Many2one('logic.base.batch',string="Batch",required=True)
    date = fields.Date(string="Date",required=True)
    student_presentations = fields.One2many('logic.student.presentation','presentation_id',string='Presentations')
    total_students = fields.Integer(string="Total Strength",compute="get_total_students" ,readonly=True)

    @api.depends('batch_id')
    def get_total_students(self):
        # for record in self:
        if self.batch_id:
            self.total_students = self.env['logic.students'].search_count([('batch_id','=',self.batch_id.id)])
        else:
            self.total_students = 0
    presentation_count = fields.Integer(string="Students Presented",compute="_compute_presentation_count")
    def _compute_presentation_count(self):
        for record in self:
            record.presentation_count = len(record.student_presentations)

class StudentPresentation(models.Model):
    _name="logic.student.presentation"
    student_id = fields.Many2one('logic.students',string="Student",required=True)
    presentation_id = fields.Many2one('logic.presentations',string="Presentation")
    feedback = fields.Text(string="Feedback")
    rating = fields.Selection(selection=[('0','No rating'),('1','Very Poor'),('2','Poor'),('3','Average'),('4','Good'),('5','Very Good')], string="Rating", default='0')
    batch_id = fields.Many2one('logic.base.batch',string="Batch")
