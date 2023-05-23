from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Create a DeclarativeMeta instance
Base = declarative_base()

# Create a sqlite engine instance
engine = create_engine("sqlite:///todo.db")

# Create SessionLocal class from sessionmaker factory
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
session = SessionLocal()
