from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from fastapi import FastAPI
from .models import Conversation

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Database configuration
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def shut_down_session():
    SessionLocal.close()

# Create tables in the database at application startup
def init_db():
    SQLModel.metadata.create_all(bind=engine)

# Linking the shutdown event to the FastAPI application
def register_shutdown_event(app: FastAPI):
    @app.on_event("shutdown")
    def shutdown():
        shut_down_session()

def create_tables():
    SQLModel.metadata.create_all(bind=engine)
