from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from .bot import chat
from .models import Conversation
from sqlalchemy.orm import session
from .database import get_db
import requests


router = APIRouter()

class EventQuery(BaseModel):
    event_id: str
class Query(BaseModel):
    query: str
event_ids = [
    "924471217297", "932778063297", "781315755457", "923043216107", "793158958797", 
    "779466975707", "866379744137", "777857772537", "910921449577", "939849454017", 
    "775002462227", "851785422127", "781315755457", "793158958797", "910933997107", 
    "871844208497", "924016687787", "910938340097", "881043062517", "881057285057"
]
def fetch_event_details(event_id):
    try:
        headers = {
            "Authorization": "Bearer K4CJXEYF2H7M6FTX5YBK",
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

@router.post("/chat")
def handle_chat(query: Query, db: session = Depends(get_db)):
    
    response = chat(query.query)
    user_message = str(query.query)
    bot_response = str(response["response"])
    #save the conversation in the database
    conversation = Conversation(user_message=user_message, bot_response=bot_response)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return response
