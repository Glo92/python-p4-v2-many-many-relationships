#!/usr/bin/env python3
# server/seed.py

import datetime
from app import app
from models import db, Employee, Meeting, Project, employee_meetings

with app.app_context():

    db.session.query(employee_meetings).delete()
    db.session.commit()
    Employee.query.delete()
    Meeting.query.delete()
    Project.query.delete()

    # Delete all rows in tables
    Employee.query.delete()
    Meeting.query.delete()
    Project.query.delete()

    # Add employees
    e1 = Employee(name="Uri Lee", hire_date=datetime.datetime(2022, 5, 17))
    e2 = Employee(name="Tristan Tal", hire_date=datetime.datetime(2020, 1, 30))
    e3 = Employee(name="Sasha Hao", hire_date=datetime.datetime(2021, 12, 1))
    e4 = Employee(name="Taylor Jai", hire_date=datetime.datetime(2015, 1, 2))
    db.session.add_all([e1, e2, e3, e4])
    db.session.commit()

    # Add meetings
    m1 = Meeting(topic="Software Engineering Weekly Update",
                 scheduled_time=datetime.datetime(
                     2023, 10, 31, 9, 30),
                 location="Building A, Room 142")
    m2 = Meeting(topic="Github Issues Brainstorming",
                 scheduled_time=datetime.datetime(
                     2023, 12, 1, 15, 15),
                 location="Building D, Room 430")
    db.session.add_all([m1, m2])
    db.session.commit()

    # Add projects
    p1 = Project(title="XYZ Project Flask server",  budget=50000)
    p2 = Project(title="XYZ Project React UI", budget=100000)
    db.session.add_all([p1, p2])
    db.session.commit()

    # Many-to-many relationship between employee and meeting
        # Add meetings to an employee
    e1.meetings.append(m1)
    e1.meetings.append(m2)
    # Add employees to a meeting
    m2.employees.append(e2)
    m2.employees.append(e3)
    m2.employees.append(e4)
    db.session.commit()

    # Many-to-many relationship between employee and project through assignment


# models.py

# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData

# metadata = MetaData()

# db = SQLAlchemy(metadata=metadata)

# class Goal(db.Model):
#     __tablename__ = 'goals'

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text)
#     target_date = db.Column(db.Date)
#     achieved = db.Column(db.Boolean, default=False)

#     goals = db.relationship('Goal', backref='user', lazy=True)


#     def to_dict(self):
#         return {
#             'id': self.id,
#             'title': self.title,
#             'description': self.description,
#             'target_date': self.target_date,
#             'achieved': self.achieved
#         }
    

#     def __repr__(self):
#         return f'<Goal {self.id}, {self.User_id}, {self.title}, {self.description}, {self.target_date}, {self.achieved}>' 

# app.py

# from flask import Flask, request
# from flask_restful import Api, Resource
# from flask_migrate import Migrate

# from models import db, Goal

# app  = Flask (__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/gloria/Desktop/Development/code/phase-4/Safe-Health/backend/instance/app.db'

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# api = Api(app)
# migrate = Migrate(app, db)
# db.init_app(app)



class GoalListResource(Resource):
    def get(self):
        goals = Goal.query.all()
        goals_list = [{'id': goal.id, 'title': goal.title, 'description': goal.description,
                       'target_date': goal.target_date.strftime('%Y-%m-%d') if goal.target_date else None,
                       'achieved': goal.achieved} for goal in goals]
        return goals_list
  

    def post(self):
        data = request.get_json()
        new_goal = Goal(title=data['title'], description=data['description'],
                        target_date=data['target_date'], achieved=data['achieved'])
        db.session.add(new_goal)
        db.session.commit()
        return {'message': 'Goal added successfully'}, 201 


    def put(self, goal_id):
        data = request.get_json()
        goal = Goal.query.get(goal_id)
        if not goal:
            return {'message': 'Goal not found'}, 404  
        goal.title = data['title']
        goal.description = data['description']
        goal.target_date = data['target_date']
        goal.achieved = data['achieved']
        db.session.commit()
        return {'message': 'Goal updated successfully'}


    def delete(self, goal_id):
        goal = Goal.query.get(goal_id)
        if not goal:
            return {'message': 'Goal not found'}, 404
        db.session.delete(goal)
        db.session.commit()
        return {'message': 'Goal deleted successfully'}

    
api.add_resource(GoalListResource, '/api/goals', endpoint='goals')
api.add_resource(GoalListResource, '/api/goals/<int:goal_id>', endpoint='goal')

if __name__== '__main__':
    app.run(port=5555,debug=True)


 