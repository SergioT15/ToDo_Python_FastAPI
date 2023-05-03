
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Boolean, Integer

# Create a sqlite engine instance
engine = create_engine("sqlite:///todo.db")

# Create a DeclarativeMeta instance
Base = declarative_base()

# Define To Do class inheriting from Base
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    completed = Column(Boolean)

