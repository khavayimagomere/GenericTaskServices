from nameko.web.handlers import http
from nameko_sqlalchemy import DatabaseSession

from src.models import Task
from src.schemas import Schema, TaskSchema, 

from marshmallow import ValidationError

class GenericTaskService:
    name = 'GenericTaskService'

    @http('GET', '/Tasks/list')
    def list_Tasks(self):
        db = Db()
        tasks = db.list_tasks()
        return TaskSchema().dumps(tasks, many = True)


    @http('POST', '/tasks/assign')
    def add_task(self, request):
        db = Db()
        created_task = db.add_task(task)
        return TaskSchema().dumps(created_task)


    @http('POST', '/task/edit_task/<uuid:value>')
    def edit_task(self, request, value):
        db.Db()
        task = db.get_task_by_id(value)
        if task:
            db.edit_task()
        return TaskSchema().dumps(task)

   
   
   

   