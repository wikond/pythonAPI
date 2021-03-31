import csv
import sys
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow
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
#ma = Marshmallow(app)

# Product Class/Model


class Department(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(100), unique=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name


def add_department(csv_record):
    dep_id = csv_record[0]
    dep_name = csv_record[1]
    new_department = Department(dep_id, dep_name)

    db.session.add(new_department)
    db.session.commit()


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


def add_project(csv_record):
    proj_id = csv_record[0]
    proj_name = csv_record[1]
    proj_client = csv_record[2]
    proj_department = csv_record[3]
    new_project = Project(proj_id, proj_name, proj_client, proj_department)

    db.session.add(new_project)
    db.session.commit()


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


def add_employee(csv_record):
    e_email = csv_record[0]
    e_lastname = csv_record[1]
    e_firstname = csv_record[2]
    e_age = csv_record[3]
    e_department = csv_record[4]
    new_employee = Employee(e_email, e_lastname,
                            e_firstname, e_age, e_department)

    db.session.add(new_employee)
    db.session.commit()


# passing arguments from CLI
args = sys.argv
for arg in args:
    if arg.find('.csv') != -1:
        file_name = arg
        records = []
        with open(file_name, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            header = next(reader)
            for row in reader:
                records.append(row)
            # print(records)
            # print(records[0][1])
            if header.__len__() == 2:
                print("Adding Departments")
                for rec in records:
                    print(rec)
                    add_department(rec)
            if header.__len__() == 5:
                print("Adding Employees")
                for rec in records:
                    print(rec)
                    add_employee(rec)
            if header.__len__() == 4:
                print("Adding Projects")
                for rec in records:
                    print(rec)
                    add_project(rec)
        csv_file.close()
