from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    query: str

@app.get("/")
def read_root():

    return {"Hello": "World"}
    
@app.post("/query")
def handle_query(query: Query):
    #logic to manage querys

    return {"response": f"Recived query: {query.query}"}