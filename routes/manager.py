from flask import Blueprint, request, jsonify
from services.manager import (
    view_manager_timesheets, approve_reject_timesheet,
    delete_timesheets, view_all_employees, update_employee_details
)
from flask_jwt_extended import jwt_required
from models.timesheet import TimesheetStatus


manager_bp = Blueprint('manager', __name__)


@manager_bp.route('/timesheets', methods=['GET'])
@jwt_required()
def view_manager_timesheets_route():
    data = request.args
    employee_name = data.get('employee_name')
    employee_id = data.get('employee_id')
    date = data.get('date')

    timesheets, error = view_manager_timesheets(employee_name, employee_id, date)
    if error:
        return jsonify(message=error), 400

    return jsonify([timesheet.serialize() for timesheet in timesheets])



@manager_bp.route('/timesheet/<int:timesheet_id>', methods=['PUT'])
@jwt_required()
def approve_reject_timesheet_route(timesheet_id):
    data = request.json
    status = data.get('status')
    comments = data.get('comments')

    timesheet, error = approve_reject_timesheet(timesheet_id, status, comments)
    if error:
        return jsonify(message=error), 400

    return jsonify(timesheet.serialize())



@manager_bp.route('/timesheets', methods=['DELETE'])
@jwt_required()
def delete_timesheets_route():
    data = request.json
    timesheet_ids = data.get('timesheet_ids')

    _, error = delete_timesheets(timesheet_ids)
    if error:
        return jsonify(message=error), 400

    return jsonify(message='Timesheets deleted successfully')



@manager_bp.route('/employees', methods=['GET'])
@jwt_required()
def view_all_employees_route():
    employees, error = view_all_employees()
    if error:
        return jsonify(message=error), 400

    return jsonify([employee.serialize() for employee in employees])



@manager_bp.route('/employe/<int:employee_id>', methods=['PUT'])
@jwt_required()
def update_employee_details_route(employee_id):
    data = request.json

    employee, error = update_employee_details(employee_id, **data)
    if error:
        return jsonify(message=error), 400

    return jsonify(employee.serialize())