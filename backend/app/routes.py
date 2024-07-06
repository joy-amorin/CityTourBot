from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .bot import chat 



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

@router.post("/event")
def get_event_details(event_query: EventQuery):
    from .main import fetch_event_details, format_event_response
    event_id = event_query.event_id.lower()

    event_data = fetch_event_details(event_id)
    if event_data:
        return format_event_response(event_data)
    else:
        raise HTTPException(status_code=404, detail=f"Evento {event_id} no encontrado")

@router.get("/events")
def get_all_events():
    from .main import fetch_event_details, format_event_response
    events = []
    for event_id in event_ids:
        event_data = fetch_event_details(event_id)
        if event_data:
            events.append(format_event_response(event_data))
    return {"events": events}

@router.post("/chat")
def handle_chat(query: Query):
    response = chat(query.query)
    return response
