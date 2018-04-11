import datetime
import uuid
from sqlalchemy import create_engine
from nameko_sqlalchemy import Database
from sqlalchemy import (
     Column, DateTime, ForeignKey, Integer, String, Float, Boolean
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

engine = create_engine('sqlite:///test.db', convert_unicode=True)

Base = declarative_base()
db = Database(Base)
class Task(Base):
    __tablename__ = 'tasks'

    task_id =  Column(UUIDType(binary = False), primary_key = True, default = uuid.uuid4)
    title =  Column(String(100), nullable = False) 
    assigner_id = Column(String(50), nullable = False)
    assignee_id = Column(String(50), nullable = False)
    date_created = Column(DateTime, nullable = False, default = datetime.datetime.now)
    due_date = Column(DateTime, nullable = True)
    completion_date = Column(DateTime, nullable = True)
    active = Column(Boolean, nullable = False, default = True)

    def to_json(self):
        return dict(task_id=task_id)

Base.metadata.create_all(engine)

