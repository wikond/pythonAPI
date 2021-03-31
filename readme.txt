This is test API website

This is Pyhton with Flask project 

Pipfile shows dependencies. Please install dependencies before running this test application

In order to generate sql lite database please run in python following commands:
>>> from app import db
>>> db.create_all()

See more:
https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application


In order to upload csv files with Departments, Projects and Employees records please use from CLI: 
python importCsv.py  filename.csv
where filename is proper name of the file (departments.csv, employees.csv, projects.csv). Scripts recognises based on header and file extension, which records to upload


GET API with Departments, Projects and Employees is available via:
http://localhost:5000/department
http://localhost:5000/project
http://localhost:5000/employee

API for single record with CRUD (POST, GET, PUT, DELETE):
http://localhost:5000/department/<id>
http://localhost:5000/project/<id>
http://localhost:5000/employee/<id>


Website for projects is available via:
http://localhost:5000/