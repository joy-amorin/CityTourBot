from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Middleware para permitir CORS y manejar OPTIONS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EventQuery(BaseModel):
    event_id: str

event_ids = [
        "924471217297",
        "932778063297",
        "781315755457"
    ]

@app.get("/")
def read_root():

    return {"Hello": "World"}
    
@app.post("/event")
def get_event_details(event_query: EventQuery):

    #get the query user
    event_id = event_query.event_id.lower()
    event_data = fetch_event_details(event_id)

    if event_data:
        return format_event_response(event_data)
    else:
        raise HTTPException(status_code=404, detail=f"Evento {event_id} no encontrado")

def fetch_event_details(event_id):
     
    try: 

        headers = {
                "Authorization": "Bearer TOKEN",
                "Content-Type": "application/json"
        }
     
        url =  f"https://www.eventbriteapi.com/v3/events/{event_id}/"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            event_data = response.json()
            return event_data
        else:
            return None
    except Exception as e:
        print(f"Error al obtener información del evento {event_id}: {e}")
        return None
    
@app.get("/events")
def get_all_events():
    events = []
    for event_id in event_ids:
        event_data = fetch_event_details(event_id)
        if event_data:
            events.append(format_event_response(event_data))
    return {"events": events}
    
    
def format_event_response(event_data):
    name = event_data["name"]["text"]
    description = event_data["description"]["text"]
    url = event_data["url"]
    start = event_data["start"]["local"]
    end = event_data["end"]["local"]


    formatted_event = {
       "name": name, "description": description, url: url, "start": start, "end": end,
    }
    return formatted_event