import json

from graphql_server import (HttpQueryError, default_format_error,
                           encode_execution_results, json_encode, load_json_body, run_http_query)


class PaginatedResult(object):
    def __init__(self, data, per_page, page, total_count):
        self.__per_page = per_page
        self.__page = page
        self.__total_count = total_count    
        self.response = json.dumps(   
            {
                "data" : data,
                "meta" :
                    {
                        "pagination" :
                        {
                            "per_page" : per_page,
                            "current_page" : page,
                            "has_next" : self.__has_next,
                            "has_prev": self.__has_previous,
                            "total_pages" : self.__total_pages,
                            "total_results" : total_count
                        }
                    }
            }) 
            

    @property
    def __has_next(self):
        return (self.__per_page * self.__page) < self.__total_count

    @property
    def __has_previous(self):
        return self.__page > 1

    @property
    def __total_pages(self):
        return -(-self.__total_count / self.__per_page)


class ErrorResponse:
    def __init__(self, errors_array):
        self.response = json.dumps(
            {
                "error" : True,
                "errors" : errors_array
            }
        )


def parse_body(request):
    content_type = request.mimetype
    if content_type == 'application/graphql':
        return {'query': request.data.decode('utf8')}

    elif content_type == 'application/json':
        return load_json_body(request.data.decode('utf8'))

    elif content_type in ('application/x-www-form-urlencoded', 'multipart/form-data'):
        return request.form

    return {}
