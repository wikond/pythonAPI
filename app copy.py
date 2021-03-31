from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
#import json

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

# Product Class/Model


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty


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


# Product Schema


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')


class ProjectSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'client', 'department')


class DepartmentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('email', 'firstname', 'lastname', 'age', 'department')


# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

# Create a Product


@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# Get All Projects


@app.route('/project', methods=['GET'])
def get_projects():
    all_projects = Project.query.all()
    result = projects_schema.dump(all_projects)
    res = jsonify(result)
    #res2 = json.dumps(result)
    return res
    # return jsonify(result.data)

# Get Single Products


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

# Get Single Products


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

# Get Single Products


@app.route('/department/<id>', methods=['GET'])
def get_department(id):
    department = Department.query.get(id)
    return department_schema.jsonify(department)

# Get All Products


@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    res = jsonify(result)
    #res2 = json.dumps(result)
    return res
    # return jsonify(result.data)


# Get Single Products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# Update a Product


@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty

    db.session.commit()

    return product_schema.jsonify(product)

# Delete Product


@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
