from flask import Blueprint, request, jsonify
from services.timesheet import fill_timesheet, view_employee_timesheets, edit_timesheet, delete_timesheet
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.timesheet import TimesheetStatus

timesheet_bp = Blueprint('timesheet', __name__)


@timesheet_bp.route('/fill', methods=['POST'])
@jwt_required()
def fill_timesheet_route():
    data = request.json
    current_user = get_jwt_identity()
    employee_id = current_user['id']

    timesheet, error = fill_timesheet(employee_id, **data)
    if error:
        return jsonify(message=error), 400

    return jsonify(timesheet.serialize()), 201


@timesheet_bp.route('/view', methods=['GET'])
@jwt_required()
def view_employee_timesheets_route():
    current_user = get_jwt_identity()
    employee_id = current_user['id']

    timesheets, error = view_employee_timesheets(employee_id)
    if error:
        return jsonify(message=error), 400

    return jsonify([timesheet.serialize() for timesheet in timesheets])


@timesheet_bp.route('/edit/<int:timesheet_id>', methods=['PUT'])
@jwt_required()
def edit_timesheet_route(timesheet_id):
    data = request.json
    current_user = get_jwt_identity()
    employee_id = current_user['id']

    timesheet, error = edit_timesheet(timesheet_id, **data)
    if error:
        return jsonify(message=error), 400

    return jsonify(timesheet.serialize())


@timesheet_bp.route('/delete/<int:timesheet_id>', methods=['DELETE'])
@jwt_required()
def delete_timesheet_route(timesheet_id):
    current_user = get_jwt_identity()
    employee_id = current_user['id']

    response, error = delete_timesheet(timesheet_id)
    if error:
        return jsonify(message=error), 400

    return jsonify(message='Timesheet deleted successfully')

