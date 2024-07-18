import json

# Global variable for storing the status of the conversation
#conversation_state = {"last_question": None}

def handle_unrecognized_month(user_query, conversation_state):
    conversation_state["last_question"] = "evento_presencial_mes"
    return {"message": f"Lo siento, no entendí el mes que quieres consultar en '{user_query}', inténtalo de nuevo.\nPuedes escribir 'exit' para volver al inicio."}, conversation_state

def handle_unrecognized_event_type(user_query, conversation_state):
    conversation_state["last_question"] = "tipo_evento"
    return {"message": f"Lo siento, no entendí qué tipo de evento quieres consultar en '{user_query}'. ¿Quieres consultar eventos presenciales u online?\nPuedes escribir 'exit' para volver al inicio."}, conversation_state

def get_online_events_response(conversation_state):
    from .routes import get_online_events
    events = get_online_events()
    conversation_state["last_question"] = "preguntar_evento_presencial"
    if events:
        return {
            "message": "Aquí están los eventos online disponibles. Si deseas más detalles, puedes entrar al link!!!",
            "events": events,
            "query_next_month": "¿Te gustaría ver eventos presenciales también? Responde 'sí' o 'no'.",
            "exit_message": "Puedes escribir 'exit' para volver al inicio."
        }, conversation_state
    else:
        return handle_unrecognized_event_type("", conversation_state)

def get_events_this_month_response(conversation_state):
    from .routes import events_this_month
    events = events_this_month()
    if events:
        conversation_state["last_question"] = "preguntar_otro_mes"
        return {
            "message": "¡Claro! Te mostraré los eventos de interés de este mes:",
            "events": events,
            "query_next_month": "¿Te gustaría ver eventos de otro mes? Responde 'sí' o 'no'.",
            "exit_message": "Puedes escribir 'exit' para volver al inicio."
        }, conversation_state
    else:
        conversation_state["last_question"] = "preguntar_otro_mes"
        return {
            "message": "No hay eventos disponibles para el mes actual, pero puedes intentar luego y ver si hay novedades.",
            "query_next_month": "¿Te gustaría ver eventos de otro mes? Responde 'sí' o 'no'.",
            "exit_message": "Puedes escribir 'exit' para volver al inicio."
        }, conversation_state

def get_events_by_specific_month_response(user_query, conversation_state):
    from .routes import extract_month_from_query, get_events_by_specific_month
    month = extract_month_from_query(user_query)
    if month:
        events = get_events_by_specific_month(month)
        if events:
            conversation_state["last_question"] = "preguntar_otro_mes"
            return {
                "message": f"¡Claro! Te mostraré los eventos de interés del mes {user_query}:",
                "events": events,
                "query_next_month": "¿Te gustaría ver eventos de otro mes? Responde 'sí' o 'no'.",
                "exit_message": "Puedes escribir 'exit' para volver al inicio."
            }, conversation_state
        else:
            conversation_state["last_question"] = "preguntar_otro_mes"
            return {
                "message": f"No hay eventos disponibles para el mes {user_query}, pero puedes intentar luego y ver si hay novedades!!",
                "query_next_month": "¿Te gustaría ver eventos de otro mes? Responde 'sí' o 'no'.",
                "exit_message": "Puedes escribir 'exit' para volver al inicio."
            }, conversation_state
    else:
        return handle_unrecognized_month(user_query, conversation_state)

def chat(query,conversation_state):
    #global conversation_state
    user_query = query.lower()


    # Check if user wants to start over
    if user_query == "exit":
        conversation_state["last_question"] = "tipo_evento"
        return {"message": "¡Has vuelto al inicio! ¿Qué tipo de eventos te gustaría conocer?\nEventos presenciales\nEventos online"}, conversation_state

    # Initial greeting and first question
    if conversation_state["last_question"] is None:
        if user_query in ["hola", "hi", "buenos días", "buenas tardes", "buenas noches"]:
            conversation_state["last_question"] = "tipo_evento"
            return {"message": "¡Hola! Soy tu chatbot de eventos. ¿Qué tipo de eventos te gustaría conocer?\n1. Eventos presenciales\n2. Eventos online"}, conversation_state

    # Handling of first question
    if conversation_state["last_question"] == "tipo_evento":
        if user_query in ["eventos presenciales", "presenciales", "presencial", "en persona", "físicos"]:
            conversation_state["last_question"] = "evento_presencial_mes"
            return {"message": "¿Quieres ver los eventos locales del mes actual o de algún otro mes?\nPuedes escribir 'exit' para volver al inicio."}, conversation_state
        
        elif user_query in ["eventos online", "online", "virtual", "virtuales", "en linea", "en línea"]:
            return get_online_events_response(conversation_state)
        else:
            # If the answer is not valid, repeat the question
            return handle_unrecognized_event_type(user_query, conversation_state)

    # Handling of the response to the question about on-site events
    if conversation_state["last_question"] == "evento_presencial_mes":
        if user_query in ["mes actual", "actual", "este mes"]:
            return get_events_this_month_response(conversation_state)
        
        # Specific month query
        elif any(month in user_query for month in ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "setiembre", "octubre", "noviembre", "diciembre"]):
            return get_events_by_specific_month_response(user_query,conversation_state)
        else:
            # If the answer is not valid, repeat the question
            return handle_unrecognized_month(user_query, conversation_state)

    # Handling of asking for another month
    if conversation_state["last_question"] == "preguntar_otro_mes":
        if "si" in user_query or "sí" in user_query:
            conversation_state["last_question"] = "evento_presencial_mes"
            return {"message": "¿Qué mes te gustaría consultar?\nPuedes escribir 'exit' para volver al inicio."}, conversation_state
        elif "no" in user_query:
            conversation_state["last_question"] = "tipo_evento"
            return {"message": "¡Entendido! ¿Qué tipo de eventos te gustaría conocer?\nEventos presenciales\nEventos online\nPuedes escribir 'exit' en cualquier momento para volver al inicio."}, conversation_state
        else:
            return {"message": "¿Te gustaría ver eventos de otro mes? Responde con 'sí' o 'no'.\nPuedes escribir 'exit' en cualquier momento para volver al inicio."}, conversation_state

    # Handling of asking about on-site events after online events
    if conversation_state["last_question"] == "preguntar_evento_presencial":
        if "si" in user_query or "sí" in user_query:
            conversation_state["last_question"] = "evento_presencial_mes"
            return {"message": "¿Quieres ver los eventos locales del mes actual o de algún otro mes?\nPuedes escribir 'exit' en cualquier momento para volver al inicio."}, conversation_state
        elif "no" in user_query:
            conversation_state["last_question"] = "tipo_evento"
            return {"message": "¡Entendido! ¿Qué tipo de eventos te gustaría conocer?\nEventos presenciales\nEventos online\nPuedes escribir 'exit' en cualquier momento para volver al inicio."},conversation_state
        else:
            return {"message": "¿Te gustaría consultar eventos presenciales también? Responde con 'sí' o 'no'.\nPuedes escribir 'exit' en cualquier momento para volver al inicio."}, conversation_state

    # Default response for unrecognized entries
    return {"message": "Lo siento, no entendí tu pregunta.\nPuedes escribir 'exit' en cualquier momento para volver al inicio."}, conversation_state
