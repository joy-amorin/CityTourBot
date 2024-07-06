
def chat(query):
    user_query = query.lower()

    if "lista de todos los eventos" in user_query:
        from .routes import get_all_events
        events = get_all_events()
        if events:
            return {"response": events}
        else:
            return {"response": "No hay eventos disponibles"} 
    else:
        return {"response": "Lo siento no puedo responder esa consulta"}