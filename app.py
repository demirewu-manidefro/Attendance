from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models import User, Group, SubGroup, Employee, Attendance
from config import Config
from datetime import datetime
import pandas as pd
import io
import matplotlib.pyplot as plt
import base64

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# -------------------------
# HOME
# -------------------------
@app.route('/')
def home():
    return redirect(url_for('login'))

# -------------------------
# LOGIN / LOGOUT
# -------------------------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            session['group_id'] = user.group_id
            session['sub_group_id'] = user.sub_group_id
            flash("Login successful", "success")
            return redirect(url_for('dashboard'))
        flash("Invalid credentials", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for('login'))

# -------------------------
# DASHBOARD
# -------------------------
@app.route('/dashboard')
def dashboard():
    role = session.get('role')
    if role == 'manager':
        return render_template('manager_dashboard.html')
    elif role == 'group_leader':
        return render_template('group_leader_dashboard.html')
    elif role == 'sub_group_leader':
        return render_template('sub_group_leader_dashboard.html')
    flash("Unauthorized access", "danger")
    return redirect(url_for('login'))

# -------------------------
# MANAGER: Add Group Leader
# -------------------------
@app.route('/add_group_leader', methods=['GET','POST'])
def add_group_leader():
    if session.get('role') != 'manager':
        flash("Unauthorized", "danger")
        return redirect(url_for('dashboard'))
    groups = Group.query.all()
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        group_id = request.form['group_id']
        user = User(username=username, password=password, role='group_leader', group_id=group_id)
        db.session.add(user)
        db.session.commit()
        flash("Group Leader added", "success")
        return redirect(url_for('dashboard'))
    return render_template('add_group_leader.html', groups=groups)

# -------------------------
# GROUP LEADER: Add Sub-Group Leader
# -------------------------
@app.route('/add_sub_group_leader', methods=['GET','POST'])
def add_sub_group_leader():
    if session.get('role') != 'group_leader':
        flash("Unauthorized", "danger")
        return redirect(url_for('dashboard'))
    subgroups = SubGroup.query.filter_by(group_id=session.get('group_id')).all()
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        sub_group_id = request.form['sub_group_id']
        user = User(username=username, password=password, role='sub_group_leader', sub_group_id=sub_group_id)
        db.session.add(user)
        db.session.commit()
        flash("Sub-Group Leader added", "success")
        return redirect(url_for('dashboard'))
    return render_template('add_sub_group_leader.html', subgroups=subgroups)

# -------------------------
# SUB-GROUP LEADER: Add Employee
# -------------------------
@app.route('/add_employee', methods=['GET','POST'])
def add_employee():
    if session.get('role') != 'sub_group_leader':
        flash("Unauthorized", "danger")
        return redirect(url_for('dashboard'))
    sub_group_id = session.get('sub_group_id')
    if request.method == 'POST':
        name = request.form['name']
        father_name = request.form['father_name']
        sex = request.form['sex']
        religion = request.form['religion']
        department = request.form['department']
        last_emp = Employee.query.filter_by(sub_group_id=sub_group_id).order_by(Employee.id.desc()).first()
        next_id = 1 if not last_emp else last_emp.id + 1
        emp_code = f"{SubGroup.query.get(sub_group_id).name}-{next_id:03d}"
        employee = Employee(
            name=name, father_name=father_name, sex=sex,
            religion=religion, department=department,
            sub_group_id=sub_group_id
        )
        db.session.add(employee)
        db.session.commit()
        flash(f"Employee {emp_code} added successfully", "success")
        return redirect(url_for('dashboard'))
    return render_template('add_employee.html')

# -------------------------
# ATTENDANCE
# -------------------------
@app.route('/attendance/<int:sub_group_id>', methods=['GET','POST'])
def attendance(sub_group_id):
    if session.get('role') not in ['manager','group_leader','sub_group_leader']:
        flash("Unauthorized", "danger")
        return redirect(url_for('dashboard'))
    employees = Employee.query.filter_by(sub_group_id=sub_group_id).all()
    if request.method == 'POST':
        date = request.form['date']
        for emp in employees:
            status = request.form.get(f'status_{emp.id}', 'Absent')
            att = Attendance(employee_id=emp.id, date=date, status=status, marked_by=session['user_id'])
            db.session.add(att)
        db.session.commit()
        flash("Attendance saved", "success")
        return redirect(url_for('dashboard'))
    return render_template('attendance.html', employees=employees)

# -------------------------
# STATISTICS & EXPORT
# -------------------------
@app.route('/attendance_report')
def attendance_report():
    if session.get('role') not in ['manager','group_leader']:
        flash("Unauthorized", "danger")
        return redirect(url_for('dashboard'))

    # Prepare dataframe
    data = []
    employees = Employee.query.all()
    for emp in employees:
        att = Attendance.query.filter_by(employee_id=emp.id).all()
        total_days = len(att)
        present_days = len([a for a in att if a.status=='Present'])
        percent = round((present_days/total_days)*100,2) if total_days>0 else 0
        data.append({
            'Employee': emp.name,
            'SubGroup': emp.subgroup.name,
            'Total Days': total_days,
            'Present Days': present_days,
            'Attendance %': percent
        })

    df = pd.DataFrame(data)
    # Export to Excel
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Attendance')
    writer.save()
    output.seek(0)
    return send_file(output, attachment_filename="attendance_report.xlsx", as_attachment=True)

# -------------------------
# CREATE DATABASE
# -------------------------
@app.cli.command("create_db")
def create_db():
    db.create_all()
    print("✅ Database tables created successfully")

# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
