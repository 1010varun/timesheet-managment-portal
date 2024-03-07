from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from models.employee import Employee
from config.configdb import db
from flask import request, jsonify

bcrypt = Bcrypt()


def generate_access_token(user_id, role):
    identity = {'id': user_id, 'role': role}
    access_token = create_access_token(identity=identity)
    return access_token


def register(data):
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    address = data.get('address')
    pan_number = data.get('pan_number')
    if not name or not email or not password or not role:
        return jsonify(message='Missing required fields'), 400

    if Employee.query.filter_by(email=email).first():
        return jsonify(message='Email already exists. Please use a different email.'), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = Employee(
        name=name,
        email=email,
        password=hashed_password,
        role=role,
        address = address,
        pan_number = pan_number
    )
    db.session.add(new_user)
    db.session.commit()
    access_token = generate_access_token(new_user.id, new_user.role)

    return access_token


def login(email, password):
    user = Employee.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = generate_access_token(user.id, user.role)
        return jsonify({
            "access_token":access_token,
            "role": user.role,
            "name": user.name,
            "email": user.email,
            "id": user.id
                        }), 200
    else:
        return jsonify(message='Invalid credentials'), 401


def reset_password(email, new_password):
    user = Employee.query.filter_by(email=email).first()

    if user:
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        return jsonify(message='Password reset successfully'), 200
    else:
        return jsonify(message='User not found'), 404


def view_employee_profile(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return None, "Employee not found"

    return employee, None


def update_employee_profile(employee_id, address, pan_number):
    employee = Employee.query.get(employee_id)
    if not employee:
        return None, "Employee not found"

    employee.address = address
    employee.pan_number = pan_number

    db.session.commit()

    return employee, None