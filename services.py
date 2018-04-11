from nameko.web.handlers import http
from nameko_sqlalchemy import DatabaseSession
from models import Task, engine
from schema import Schema, TaskSchema
from models import db

from marshmallow import ValidationError
from sqlalchemy.orm import sessionmaker
import json

class GenericTaskService:
    name = 'GenericTaskService'

    Session = sessionmaker(bind=engine)
    db = Session()

    @http('GET', '/tasks/list')
    def list_tasks(self, request):
        tasks = self.db.query(Task).all()
        return TaskSchema().dumps(tasks, many = True).data


    @http('POST', '/tasks/add')
    def add_task(self, request):
        created_task =self.db.add(Task)
        self.db.commit()
        return TaskSchema().dumps(created_task).data


    @http('PUT', '/tasks/edit_task/<uuid:value>')
    def edit_task(self, request, value):
        db.Db()
        task = db.get_task_by_id(value)
        if task:
            db.edit_task()
        return TaskSchema().dumps(task)

   
   
   

