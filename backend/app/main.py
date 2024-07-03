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

class Query(BaseModel):
    query: str

@app.get("/")
def read_root():

    return {"Hello": "World"}
    
@app.post("/query")
def handle_query(query: Query):

    #get the query user
    user_query = query.query.lower()

    #verify the query type and handle it properly
    if "clima" in user_query or "tiempo" in user_query:
        city = extract_city(user_query)
        if city:
            weather_data = get_weather(city)
            return {"response": f"El clima en {city.capitalize()} es {weather_data['weather']}"}
        else:
            raise HTTPException(status_code=400, detail="Porfavor especifica una ciudad válid para consultar el clima")
    else: 
        return {"response": "Lo siento, no puedo responder esa consulta"}
    
def extract_city(query):
    cities = ["montevideo", "buenos aires", "madrid"]
    for city in cities:
        if city in query:
            return city
    return None
    
def get_weather(city):
    api_key = "ddb8b8da152ed986f3f270a8ab4ca2a8"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(base_url)
        data = response.json()
        weather = data["weather"][0]["description"]
        return {"weather": weather}
    except Exception as e:
        print(f"Error sl obtener el clima para {city}: e")
        return {"weather": "no disponible"}