from sqlalchemy.orm import sessionmaker
from nameko.web.handlers import http

from app.models import Task, engine, create_all_tables
from app.schema import TaskSchema


class GenericTaskService:
    name = 'generic-task-service'
    create_all_tables(engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    @http('GET', '/tasks')
    def list_tasks(self, request):
        tasks = self.db.query(Task).all()
        return TaskSchema().dumps(tasks, many=True).data


    @http('POST', '/tasks')
    def add_task(self, request):
        new_task = TaskSchema().loads(request.data).data
        self.db.add(new_task)
        self.db.commit()
        return TaskSchema().dumps(new_task).data

    
    @http('POST', '/tasks/<uuid:value>')
    def get_task(self, request, value):
        pass
