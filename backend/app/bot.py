
def chat(query):
    user_query = query.lower()

    if "lista de todos los eventos" in user_query:
        from .routes import get_all_events
        events = get_all_events()
        if events:
            return {"response": events}
        else:
            return {"response": "No hay eventos disponibles"}
        
    if "eventos de este mes" in user_query:
        from .routes import events_this_month
        events = events_this_month()
        if events:
            return {"response": events}
        else:
            return {"response": "No hay eventos disponibles para este mes"}
    else:
        from .routes import extract_month_from_query
        month = extract_month_from_query(user_query)
        if month:
            from .routes import get_events_by_specific_month
            events = get_events_by_specific_month(month)
            if events:
                return {"response": events}
            else:
                return f"no hay eventos para el mes {month}"
            
    return {"response": "Lo siento no puedo responder esa consulta"}
    
    