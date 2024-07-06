from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from .routes import router
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
app = FastAPI()

# Middleware para permitir CORS y manejar OPTIONS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

# Database configuration
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

Base.metadata.create_all(bind=engine) #create tables on database



@app.get("/")
def read_root():
    return {"Hello": "World"}

# Funciones que permanecen en main.py
def fetch_event_details(event_id):
    try:
        headers = {
            "Authorization": "Bearer TOKEN",
            "Content-Type": "application/json"
        }
        url = f"https://www.eventbriteapi.com/v3/events/{event_id}/"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error al obtener información del evento {event_id}: {e}")
        return None

def format_event_response(event_data):
    name = event_data["name"]["text"]
    description = event_data["description"]["text"]
    url = event_data["url"]
    start = event_data["start"]["local"]
    end = event_data["end"]["local"]

    formatted_event = {
        "name": name,
        "description": description,
        "url": url,
        "start": start,
        "end": end,
    }
    return formatted_event
