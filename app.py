from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.configdb import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta

from models.employee import Employee
from models.timesheet import Timesheet

from routes.employee import employee
from routes.timesheet import timesheet_bp
from routes.manager import manager_bp


app = Flask(__name__)
CORS(app, origins="*")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_new_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "sample secret key"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=90)
jwt = JWTManager(app)


db.init_app(app)

app.register_blueprint(employee, url_prefix='/employee')
app.register_blueprint(timesheet_bp, url_prefix='/timesheet')
app.register_blueprint(manager_bp, url_prefix='/manager')


try:
    with app.app_context():
        db.create_all()
        print("tables created successfully")

except: 
    print("error occured while creating tables")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
