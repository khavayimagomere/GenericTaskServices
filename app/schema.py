import uuid
import datetime
from sqlalchemy import (
   Column, DateTime, String, Boolean, Float, UniqueConstraint
)
from app.models import Task, Session, Base
from marshmallow import Schema, fields, post_load
from marshmallow import validate
from marshmallow_sqlalchemy.convert import ModelConverter
from marshmallow.exceptions import ValidationError
from sqlalchemy_utils import UUIDType

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from graphene_sqlalchemy.converter import convert_sqlalchemy_type, get_column_doc, is_column_nullable
from graphene import (String)
import graphene_sqlalchemy.tests



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

Base.query = Session.query_property()

#schemas
class TaskSchema(Schema):
    task_id = UUIDTypeSerializationField(dump_only=True)
    title =   fields.String(validate=not_blank)
    assigner_id = fields.String(validate=not_blank)
    assignee_id = fields.String()
    date_created = fields.DateTime()
    due_date = fields.DateTime()
    completion_date = fields.DateTime()
    active = fields.Boolean()

    
    class Meta:
        model_converter = UUIDTypeConverter
        model = Task


    @post_load
    def deserialize_to_object(self, data):
        return Task(**data)

@convert_sqlalchemy_type.register(UUIDType)
def convert_column_to_string(type, column, registry=None):
    return String(description=get_column_doc(column),
                  required=not(is_column_nullable(column)))


class TaskGQL(SQLAlchemyObjectType):
    class Meta:
        model = Task
        interfaces = (relay.Node,)

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    tasks = graphene.List(TaskGQL, description='Get list of tasks')
    task_by_id = graphene.Field(TaskGQL, task_id=graphene.String())

    def resolve_tasks(self, info):
        return TaskGQL.get_query(info).all()

    def resolve_task_by_id(self, info, **args):
        task_id = args.get('task_id')
        query = TaskGQL.get_query(info)
        return query.filter(Task.task_id == task_id).first()

g_schema = graphene.Schema(
   query=Query, types=[TaskGQL], auto_camelcase=False)
