from models.employee import Employee
from models.timesheet import Timesheet, TimesheetStatus
from config.configdb import db
from datetime import datetime

def fill_timesheet(employee_id, date, hours_spent, description, typeof, comments):
    employee = Employee.query.get(employee_id)
    if not employee:
        return None, "Employee not found"

    timesheet = Timesheet(
        date=date,
        hours_spent=hours_spent,
        employee_id=employee_id,
        description=description,
        status=TimesheetStatus.IN_PROCESS,
        comments=comments,
        typeof=typeof,
    )

    db.session.add(timesheet)
    db.session.commit()

    return timesheet, None


def view_employee_timesheets(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return None, "Employee not found"

    timesheets = Timesheet.query.filter_by(employee_id=employee_id).order_by(Timesheet.filled_on.desc()).all()

    return timesheets, None


def edit_timesheet(timesheet_id, hours_spent, description):
    timesheet = Timesheet.query.get(timesheet_id)
    if not timesheet:
        return None, "Timesheet not found"

    if timesheet.status in [TimesheetStatus.APPROVED, TimesheetStatus.REJECTED]:
        return None, "Cannot edit a timesheet that is already Approved or Rejected"

    timesheet.hours_spent = hours_spent
    timesheet.description = description

    db.session.commit()

    return timesheet, None


def delete_timesheet(timesheet_id):
    timesheet = Timesheet.query.get(timesheet_id)
    if not timesheet:
        return None, "Timesheet not found"

    if timesheet.status in [TimesheetStatus.APPROVED, TimesheetStatus.REJECTED]:
        return None, "Cannot delete a timesheet that is already Approved or Rejected"

    db.session.delete(timesheet)
    db.session.commit()

    return timesheet, None
