from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import get_db
from .models import Conversation
from .bot import chat
import requests
from datetime import datetime
import json

router = APIRouter()

class EventQuery(BaseModel):
    event_id: str

class OnlineEventQuery(BaseModel):
    online_event_id: str

class Query(BaseModel):
    query: str

event_ids = [
    "924471217297", "932778063297", "781315755457", "923043216107", "793158958797", 
    "779466975707", "866379744137", "777857772537", "910921449577", "939849454017", 
    "775002462227", "851785422127", "781315755457", "793158958797", "910933997107", 
    "871844208497", "924016687787", "910938340097", "881043062517", "881057285057",
    "942544254237"
]

online_event_ids = [
    "939475896697", "923444977787", "917343347647", "63049080497",
    "680004109597"
]

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

@router.post("/event")
def get_event_details(event_query: EventQuery):
    event_id = event_query.event_id.lower()
    event_data = fetch_event_details(event_id)
    if event_data:
        return format_event_response(event_data)
    else:
        raise HTTPException(status_code=404, detail=f"Evento {event_id} no encontrado")

@router.get("/events")
def get_all_events():
    events = []
    for event_id in event_ids:
        event_data = fetch_event_details(event_id)
        if event_data:
            events.append(format_event_response(event_data))
    return {"events": events}

@router.get("/online_events")
def get_online_events():
    online_events = []
    for online_event_id in online_event_ids:
        online_event_data = fetch_event_details(online_event_id)
        if online_event_data:
            online_events.append(format_event_response(online_event_data))
    return online_events

def extract_month_from_query(user_query):
    months = { 
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, 
        "mayo": 5, "junio": 6,"julio": 7, "agosto": 8, 
        "setiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    for month_name, month_number in months.items():
        if month_name in user_query:
            return month_number
    return None

def filter_events_by_month(month):
    all_events = get_all_events()
    filtered_events = []
    for event in all_events["events"]:
        start_date_str = event["start"]
        start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%S")
        if start_date.month == month:
            filtered_events.append(event)
    if not filtered_events:
        return None
    return {"filtered_events": filtered_events}

def events_this_month():
    current_month = datetime.now().month
    this_month_events = filter_events_by_month(current_month)
    if not this_month_events:
        return None
    return this_month_events

def get_events_by_specific_month(month):
    events_in_specific_month = filter_events_by_month(month)
    return events_in_specific_month

@router.post("/chat")
def handle_chat(query: Query, db: Session = Depends(get_db)):
    try:
        response = chat(query.query)
        user_message = query.query
        
       #save the conversation in the database
        conversation = Conversation(user_message=user_message, bot_response=str(response))
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        
        return response  # Devuelve la respuesta completa del bot

    except Exception as e:
        return {"error": str(e)}

@router.get("/conversations/")
def get_conversations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    conversations = db.query(Conversation).offset(skip).limit(limit).all()
    return conversations
