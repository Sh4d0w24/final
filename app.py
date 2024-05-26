from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Employees(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    email_address = db.Column(db.String(10), nullable=False)
    job_title = db.Column(db.String(50), nullable=False)
    business_phone = db.Column(db.String(50), nullable=False)
    home_phone = db.Column(db.String(15), nullable=False)
    mobile_phone = db.Column(db.String(100), nullable=False)

@app.route('/customers', methods=['GET'])
def get_employees():
    employees = Employees.query.all()
    return render_template('index.html', employees=employees)

@app.route('/customers/create', methods=['GET', 'POST'])
def create_employee():
    if request.method == 'POST':
        data = request.form.to_dict()
        new_employee = Employees(**data)
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for('get_employees'))
    return render_template('create.html')

@app.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    employee = Employees.query.get(id)
    if not employee:
        return jsonify({'error': 'Employee not found.'}), 404
    if request.method == 'POST':
        data = request.form.to_dict()
        for key, value in data.items():
            setattr(employee, key, value)
        db.session.commit()
        return redirect(url_for('get_employees'))
    return render_template('edit.html', employee=employee)

@app.route('/customers/delete/<int:id>', methods=['GET', 'POST'])
def delete_employee(id):
    employee = Employees.query.get(id)
    if not employee:
        return jsonify({'error': 'Employee not found.'}), 404
    if request.method == 'POST':
        db.session.delete(employee)
        db.session.commit()
        return redirect(url_for('get_employees'))
    return render_template('delete.html', employee=employee)

if __name__ == '__main__':
    app.run(debug=True)