import uuid
import datetime
from sqlalchemy import (
   Column, DateTime, String, Boolean, Float, UniqueConstraint
)
from models import Task
from marshmallow import Schema, fields
from marshmallow import validate
from marshmallow_sqlalchemy.convert import ModelConverter
from marshmallow.exceptions import ValidationError
from sqlalchemy_utils import UUIDType


#custom convertor
class UUIDTypeConverter(ModelConverter):
    SQLA_TYPE_MAPPING = dict(
        list(ModelConverter.SQLA_TYPE_MAPPING.items()) +
        [(UUIDType, fields.Str)]
    )


class UUIDTypeSerializationField(fields.Field):
    def _serialize(self, value, attr, obj):
        if value is None:
            return value
        else:
            if isinstance(value, uuid.UUID):
                return str(value)
            else:
                return None


def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


not_blank = validate.Length(min=1, error='Field cannot be blank')

#schemas
class Task(object):
    def __init__(self, title,task_id):
        self.title = title
        self.task_id = task_id


class TaskSchema(Schema):
    task_id = UUIDTypeSerializationField(dump_only=True)
    title =   Column(String(100), nullable = False)
    assigner_id = Column(String(50), nullable = False)
    assignee_id = Column(String(50), nullable = False)
    date_created = Column(DateTime, nullable = False, default = datetime.datetime.now)
    due_date = Column(DateTime, nullable = True)
    completion_date = Column(DateTime, nullable = True)
    active = Column(Boolean, nullable = False, default = True) 

    
    class Meta:
        model_converter = UUIDTypeConverter
        model = Task




