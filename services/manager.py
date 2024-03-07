from models.employee import Employee
from models.timesheet import Timesheet, TimesheetStatus 
from models.employee import Employee
from config.configdb import db
from flask_jwt_extended import jwt_required, get_jwt_identity


def view_manager_timesheets(employee_name=None, employee_id=None, date=None):
    query = Timesheet.query.order_by(Timesheet.filled_on.desc())

    if employee_name:
        query = query.join(Employee).filter(Employee.name.ilike(f"%{employee_name}%"))
    if employee_id:
        query = query.filter(Timesheet.employee_id == employee_id)
    if date:
        query = query.filter(Timesheet.date == date)

    timesheets = query.all()

    return timesheets, None


def approve_reject_timesheet(timesheet_id, status, comments=None):
    timesheet = Timesheet.query.get(timesheet_id)
    if not timesheet:
        return None, "Timesheet not found"

    if timesheet.status in [TimesheetStatus.APPROVED, TimesheetStatus.REJECTED]:
        return None, "Cannot modify a timesheet that is already Approved or Rejected"

    current_user = get_jwt_identity()
    manager_id = current_user['id']
    manager = Employee.query.get(manager_id)
    timesheet.status = status
    timesheet.comments = comments
    timesheet.approved_by = manager.name

    db.session.commit()
    return timesheet, None


def delete_timesheets(timesheet_ids):
    for timesheet_id in timesheet_ids:
        timesheet = Timesheet.query.get(timesheet_id)
        if timesheet:
            db.session.delete(timesheet)

    db.session.commit()

    return None, None


def view_all_employees():
    employees = Employee.query.all()
    return employees, None


def update_employee_details(employee_id, name, role, address, pan_number):
    employee = Employee.query.get(employee_id)
    if not employee:
        return None, "Employee not found"

    employee.name = name
    employee.role = role
    employee.address = address
    employee.pan_number = pan_number

    db.session.commit()

    return employee, None
