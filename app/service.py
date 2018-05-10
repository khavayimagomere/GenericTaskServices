from sqlalchemy.orm import sessionmaker
from nameko.web.handlers import http

from app.models import Task, Session
from app.schema import TaskSchema, g_schema
from app.utils import parse_body, PaginatedResult
from graphql_server import (HttpQueryError, default_format_error,
                           encode_execution_results, json_encode, load_json_body, run_http_query)


class GenericTaskService:
    name = 'generic-task-service'
    db = Session

    @http('GET', '/tasks')
    def list_tasks(self, request):
        per_page = request.args.get('page_size')
        page = request.args.get('page')
        query = self.db.query(Task).order_by(Task.title)
        
        # total number of records
        total_count = query.count()

        if(per_page):
            per_page = int(per_page)
            query = query.limit(per_page)

            current_page = int(page) if(page) else 1
           
            # add offset
            offset = (current_page - 1) * per_page
            query = query.offset(offset)

            data = TaskSchema().dump(query.all(), many=True).data
            return PaginatedResult(data, per_page, current_page, total_count).response

        all_tasks = TaskSchema().dumps(query.all(), many=True).data
        return all_tasks

    @http('POST', '/tasks')
    def add_task(self, request):
        new_task = TaskSchema().loads(request.data).data
        self.db.add(new_task)
        self.db.commit()
        return TaskSchema().dumps(new_task).data
    
    @http('GET', '/tasks/<uuid:value>')
    def get_task_by_id(self, request, value):
        task = self.db.query(Task).get(value)
        return TaskSchema().dumps(task).data
        
    @http('POST', '/graphql')
    def query(self, request):
        data  = parse_body(request)

        execution_results, all_params = run_http_query(
            g_schema,
            'post',
            data) 

        result, status_code = encode_execution_results(
            execution_results,
            format_error=default_format_error,is_batch=False, encode=json_encode)

        return result

