def chat(query):
    user_query = query.lower()

    # Saludo inicial
    if user_query in ["hola", "hi", "buenos días", "buenas tardes", "buenas noches"]:
        return {"response": "¡Hola! Soy tu chatbot de eventos. ¿Qué tipo de eventos te gustaría conocer?\n1. Eventos presenciales\n2. Eventos online"}

    # Eventos presenciales
    if "eventos presenciales" in user_query:
        return {"response": "¿Quieres ver los eventos locales del mes actual o de algún otro mes?"}

    # Eventos de este mes
    elif "eventos de este mes" in user_query:
        from .routes import events_this_month
        events = events_this_month()
        if events:
            return {"response": f"Con gusto te mostraré los eventos de interés de este mes:\n{events}"}
        else:
            return {"response": "No hay eventos disponibles para este mes por el momento, pero puedes intentar luego y ver si hay novedades."}

    # Eventos online
    elif "eventos online" in user_query:
        from .routes import get_online_events
        events = get_online_events()
        if events:
            return {"response": f"Aquí tienes los eventos online disponibles:\n{events}"}
        else:
            return {"response": "No hay eventos online disponibles por el momento, pero puedes intentar luego y ver si hay novedades."}

    # Consulta por mes específico
    else:
        from .routes import extract_month_from_query, get_events_by_specific_month
        month = extract_month_from_query(user_query)
        if month:
            events = get_events_by_specific_month(month)
            if events:
                return {"response": f"Claro, te mostraré los eventos de {month}:\n{events}"}
            else:
                return {"response": f"No hay eventos disponibles para el mes {month}, pero puedes intentar luego y ver si hay novedades."}

    # Respuesta por defecto para entradas no reconocidas
    return {"response": "Lo siento, no entendí tu pregunta. ¿Podrías ser más específico?"}
