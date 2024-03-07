from config.configdb import db
from datetime import datetime

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    role = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pan_number = db.Column(db.String(10), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_on': self.created_on.isoformat(),
            'role': self.role,
            'address': self.address,
            'pan_number': self.pan_number
        }