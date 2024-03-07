from flask import Blueprint, request, jsonify
from services.employee import *
from models.employee import Employee
from config.configdb import db
from flask_jwt_extended import jwt_required, get_jwt_identity

employee = Blueprint('employee', __name__)


@employee.route('/signup', methods=['POST'])
def signup():
    data = request.json
    access_token = register(data)
    return jsonify(access_token=access_token), 201


@employee.route('/login', methods=['POST'])
def login_employee():
    email = request.json.get('email')
    password = request.json.get('password')
    response = login(email, password)
    return response

    
@employee.route('/password', methods=['PUT'])
@jwt_required()
def reset():
    email = request.json.get('email')
    new_password = request.json.get('new_password')
    response = reset_password(email, new_password)
    return response


@employee.route('/profile', methods=['GET'])
@jwt_required()
def view_employee_profile_route():
    current_user = get_jwt_identity()
    employee_id = current_user['id']

    employee, error = view_employee_profile(employee_id)
    if error:
        return jsonify(message=error), 400

    return jsonify(employee.serialize())


@employee.route('/profile', methods=['PUT'])
@jwt_required()
def update_employee_profile_route():
    data = request.json
    current_user = get_jwt_identity()
    employee_id = current_user['id']

    employee, error = update_employee_profile(employee_id, **data)
    if error:
        return jsonify(message=error), 400

    return jsonify(employee.serialize())