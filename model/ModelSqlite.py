from sqlalchemy import Column, INTEGER, String, DATE, DATETIME,BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow
from datetime import datetime

db = SQLAlchemy()
#ma = Marshmallow()

class ModelSQLITE:
    def __init__(self, app):
        self.app = app

    def connect(self):
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///model/db/task.sqlite3'
        self.app.config['SCRET_KEY'] = 'kkkkkofsecurity'
        db.init_app(self.app)
        db.create_all(app=self.app)
        #ma.init_app(self.app)

class TaskType(db.Model):
    __tablename__ = 'tasktype'
    id = Column(INTEGER, primary_key=True)
    name = Column(String, nullable=False, default='')

    def __init__(self, name):
        self.name = name


class Action(db.Model):
    __tablename__ = 'action'
    id = Column(INTEGER, primary_key=True)
    description = Column(String, nullable=False, default='')
    init = Column(DATETIME, default=datetime.now())
    finish = Column(DATETIME, nullable=True)
    finished = Column(BOOLEAN, nullable=False, default=False)
    task_id = Column(INTEGER, ForeignKey('task.id'))


class Order(db.Model):
    __tablename__ = 'order'
    id = Column(INTEGER, primary_key=True)
    number = Column(INTEGER, nullable=False, default='0')
    client_name = Column(String)
    client_id = Column(String)
    aggregator = Column(String)   

class Task(db.Model):
    __tablename__ = 'task'
    id = Column(INTEGER, primary_key=True)
    name = Column(String, nullable=False, default='')
    day = Column(DATE, nullable=False, default=datetime.now())
    type_id = Column(INTEGER, ForeignKey('tasktype.id'))
    task_type = relationship('TaskType')
    order_id = Column(INTEGER, ForeignKey('order.id'))
    order = relationship('Order')
    actions = relationship('Action', backref='Task', lazy=False)


"""
#TODO move to outher file

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

class TypeOrderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')
"""