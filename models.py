import datetime
import uuid
from sqlalchemy import (
     Column, DateTime, ForeignKey, Integer, String, Float, Boolean
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

import config

class BaseColumn(object):
    date_created = Column(DateTime, nullable = False, default = datetime.datetime.now)
    assigner_id = Column(String(50), nullable = False)
    assignee_id = Column(String(50), nullable = False)
    due_date = Column(DateTime, nullable = True)
    completion_date = Column(DateTime, nullable = True)
    active = Column(Boolean, nullable = False, default = True)

class Task(Base):
    __tablename__ = 'tasks'

    task_id =  Column(UUIDType(binary = False), primary_key = True, default = uuid.uuid4)
    title =  Column(String(100), nullable = False) 



    