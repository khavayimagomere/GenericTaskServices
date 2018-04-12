from sqlalchemy import (
    Column, DateTime, ForeignKey, Integer, String, Float, Boolean, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.engine.url import URL
from sqlalchemy_utils import UUIDType
from sqlalchemy import create_engine
from app.settings import DATABASE_CONFIG

import datetime
import uuid

engine = create_engine(URL(**DATABASE_CONFIG))

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(UUIDType(binary=False),
                       primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable = False) 
    assigner_id = Column(String(50), nullable = False)
    assignee_id = Column(String(50), nullable = False)
    date_created = Column(DateTime, nullable = False, default = datetime.datetime.now)
    due_date = Column(DateTime, nullable = True)
    completion_date = Column(DateTime, nullable = True)
    active = Column(Boolean, nullable = False, default = True)

def create_all_tables(engine):
    Base.metadata.create_all(engine)