from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from .routes import router
from .database import init_db, register_shutdown_event
from .database import create_tables
from . import models  # Ensure models are imported

app = FastAPI()

init_db()

register_shutdown_event(app)
# Middleware para permitir CORS y manejar OPTIONS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

@app.on_event("startup")
def on_startup():
    create_tables()

@app.get("/")
def read_root():
    return {"Hello": "World"}

