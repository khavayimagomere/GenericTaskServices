import uuid
import datetime
from sqlalchemy import (
   Column, DateTime, String, Boolean, Float, UniqueConstraint
)
from app.models import Task
from marshmallow import Schema, fields, post_load
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