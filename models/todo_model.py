from sqlalchemy import create_engine, Column, String, Boolean, Integer
from db import Base

# Define To Do class inheriting from Base
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    completed = Column(Boolean)