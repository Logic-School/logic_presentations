from odoo import fields,models,api

class LogicPresentation(models.Model):
    _name="logic.presentations"
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
class StudentPresentation(models.Model):
    _name="logic.student.presentation"
    student_id = fields.Many2one('logic.students',string="Student",required=True)
    presentation_id = fields.Many2one('logic.presentations',string="Presentation")
    feedback = fields.Text(string="Feedback")
    rating = fields.Selection(selection=[('0','No rating'),('1','Very Poor'),('2','Poor'),('3','Average'),('4','Good'),('5','Very Good')], string="Rating", default='0')
    batch_id = fields.Many2one('logic.base.batch',string="Batch")
