from config.configdb import db
from datetime import datetime
from enum import Enum


class TimesheetStatus(Enum):
    IN_PROCESS = 'In Process'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'

class TimesheetType(Enum):
    LEAVE = 'Leave'
    WORK = 'Work'

class Timesheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    hours_spent = db.Column(db.Float, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Enum(TimesheetStatus), nullable=False)
    filled_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    approved_by = db.Column(db.String(100))
    comments = db.Column(db.Text)
    attachment = db.Column(db.String(100))
    typeof = db.Column(db.Enum(TimesheetType), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'hours_spent': self.hours_spent,
            'employee_id': self.employee_id,
            'description': self.description,
            'status': self.status.value,
            'filled_on': self.filled_on.isoformat(),
            'approved_by': self.approved_by,
            'comments': self.comments,
            'attachment': self.attachment,
            'type': self.typeof.value
        }
