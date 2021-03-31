from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Class/Model


class Department(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(100), unique=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name


class Project(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(100), unique=False)
    client = db.Column(db.String(100), unique=False)
    department = db.Column(db.String(100), unique=False)

    def __init__(self, id, name, client, department):
        self.id = id
        self.name = name
        self.client = client
        self.department = department


class Employee(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    lastname = db.Column(db.String(100), unique=False)
    firstname = db.Column(db.String(100), unique=False)
    age = db.Column(db.Integer, unique=False)
    department = db.Column(db.String(100), unique=False)

    def __init__(self, email, lastname, firstname, age, department):
        self.email = email
        self.lastname = lastname
        self.firstname = firstname
        self.age = age
        self.department = department


# Average employee age of department
# Employees per department
# Number of Projects per department
class Statistics(object):
    def __init__(self, name, av_age, nr_emp, nr_projects):
        self.name = name
        self.av_age = av_age
        self.nr_emp = nr_emp
        self.nr_projects = nr_projects

# Schemas


class ProjectSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'client', 'department')


class DepartmentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('email', 'firstname', 'lastname', 'age', 'department', 'pid')


# Init schema

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

# Website for Projects


@app.route('/')
def index():
    all_projects = Project.query.all()
    project_data = projects_schema.dump(all_projects)

    all_departments = Department.query.all()
    department_data = departments_schema.dump(all_departments)

    all_employees = Employee.query.all()
    employee_data = employees_schema.dump(all_employees)

    return render_template('index.html', p_data=project_data, d_data=department_data, e_data=employee_data)


@app.route('/departments/<string:id>/')
def department(id):
    all_projects = Project.query.all()
    project_data = projects_schema.dump(all_projects)

    all_departments = Department.query.all()
    department_data = departments_schema.dump(all_departments)

    all_employees = Employee.query.all()
    employee_data = employees_schema.dump(all_employees)

    return render_template('departments.html', p_data=project_data, render_data=department_data[int(id)-1], e_data=employee_data)


@app.route('/statistics/')
def statistics():
    all_projects = Project.query.all()
    project_data = projects_schema.dump(all_projects)

    all_departments = Department.query.all()
    department_data = departments_schema.dump(all_departments)

    all_employees = Employee.query.all()
    employee_data = employees_schema.dump(all_employees)
    # Average employee age of department
    # Employees per department
    # Number of Projects per department
    #name, av_age, nr_emp, nr_projects
    statistics = []
    for record_d in all_departments:
        statistics.append(Statistics(record_d.name, 0, 0, 0))
        age_counter = 0
        age_total = 0
        for record_e in all_employees:
            if record_e.department == record_d.name:
                statistics[-1].nr_emp += 1
                age_total += record_e.age
                age_counter += 1
                if age_counter != 0:
                    statistics[-1].av_age = age_total/age_counter
        for record_p in all_projects:
            if record_p.department == record_d.name:
                statistics[-1].nr_projects += 1

    return render_template('statistics.html', render_data=statistics)


@app.route('/projects/<string:id>/')
def project(id):
    all_projects = Project.query.all()
    project_data = projects_schema.dump(all_projects)
    return render_template('project.html', render_data=project_data[int(id)-1])


@app.route('/employees/<string:pid>/')
def employee(pid):
    all_employees = Employee.query.all()
    employee_data = employees_schema.dump(all_employees)
    return render_template('employees.html', render_data=employee_data[int(pid)-1])

# POST for Single  Projects, Departments and Employees


@app.route('/project', methods=['POST'])
def add_project():
    id = request.json['id']
    name = request.json['name']
    department = request.json['department']
    client = request.json['client']

    new_project = Project(id, name, client, department)

    db.session.add(new_project)
    db.session.commit()

    return project_schema.jsonify(new_project)


@app.route('/department', methods=['POST'])
def add_department():
    id = request.json['id']
    name = request.json['name']

    new_department = Department(id, name)

    db.session.add(new_department)
    db.session.commit()

    return department_schema.jsonify(new_department)


@app.route('/employee', methods=['POST'])
def add_employee():
    email = request.json['email']
    lastname = request.json['lastname']
    firstname = request.json['firstname']
    age = request.json['age']
    department = request.json['department']

    new_employee = Employee(email, lastname, firstname, age, department)

    db.session.add(new_employee)
    db.session.commit()

    return employee_schema.jsonify(new_employee)

# GET for Single and All Projects, Departments and Employees


@app.route('/project', methods=['GET'])
def get_projects():
    all_projects = Project.query.all()
    result = projects_schema.dump(all_projects)
    res = jsonify(result)
    #res2 = json.dumps(result)
    return res
    # return jsonify(result.data)


@app.route('/project/<id>', methods=['GET'])
def get_project(id):
    project = Project.query.get(id)
    return project_schema.jsonify(project)


@app.route('/department', methods=['GET'])
def get_departments():
    all_departments = Department.query.all()
    result = departments_schema.dump(all_departments)
    res = jsonify(result)
    return res


@app.route('/employee/<id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    return employee_schema.jsonify(employee)


@app.route('/employee', methods=['GET'])
def get_employees():
    all_employees = Employee.query.all()
    result = employees_schema.dump(all_employees)
    res = jsonify(result)
    return res


@app.route('/department/<id>', methods=['GET'])
def get_department(id):
    department = Department.query.get(id)
    return department_schema.jsonify(department)

# PUT - update for Single  Projects, Departments and Employees


@app.route('/project/<id>', methods=['PUT'])
def update_project(id):
    project = Project.query.get(id)

    id = request.json['id']
    name = request.json['name']
    department = request.json['department']
    client = request.json['client']

    project.id = id
    project.name = name
    project.department = department
    project.client = client

    db.session.commit()

    return project_schema.jsonify(project)


@app.route('/department/<id>', methods=['PUT'])
def update_department(id):
    department = Department.query.get(id)

    id = request.json['id']
    name = request.json['name']

    department.id = id
    department.name = name

    db.session.commit()

    return department_schema.jsonify(department)


@app.route('/employee/<id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get(id)

    email = request.json['email']
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    department = request.json['department']
    age = request.json['age']
    pid = request.json['pid']

    employee.email = email
    employee.firstname = firstname
    employee.lastname = lastname
    employee.department = department
    employee.age = age

    db.session.commit()

    return employee_schema.jsonify(employee)


@app.route('/project/<id>', methods=['DELETE'])
def delete_project(id):
    project = Project.query.get(id)
    db.session.delete(project)
    db.session.commit()

    return department_schema.jsonify(project)


@app.route('/department/<id>', methods=['DELETE'])
def delete_department(id):
    department = Department.query.get(id)
    db.session.delete(department)
    db.session.commit()

    return department_schema.jsonify(department)


@app.route('/employee/<id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)
    db.session.delete(employee)
    db.session.commit()

    return employee_schema.jsonify(employee)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
