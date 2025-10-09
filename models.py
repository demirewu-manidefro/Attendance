from db import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # manager, group_leader, sub_group_leader
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)
    sub_group_id = db.Column(db.Integer, db.ForeignKey('sub_group.id'), nullable=True)

    group = db.relationship('Group', backref='users')
    subgroup = db.relationship('SubGroup', backref='users')

class Group(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    subgroups = db.relationship("SubGroup", backref="group", lazy=True)

class SubGroup(db.Model):
    __tablename__ = "subgroups"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    employees = db.relationship("Employee", backref="subgroup", lazy=True)

class Employee(db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    religion = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sub_group_id = db.Column(db.Integer, db.ForeignKey("subgroups.id"), nullable=False)

class Attendance(db.Model):
    __tablename__ = "attendance"
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    marked_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
