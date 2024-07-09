# Global variable for storing the status of the conversation
conversation_state = {"last_question": None}

def chat(query):
    global conversation_state
    user_query = query.lower()

    # Initial greeting and first question
    if conversation_state["last_question"] is None:
        if user_query in ["hola", "hi", "buenos días", "buenas tardes", "buenas noches"]:
            conversation_state["last_question"] = "tipo_evento"
            return {"response": "¡Hola! Soy tu chatbot de eventos. ¿Qué tipo de eventos te gustaría conocer?\n1. Eventos presenciales\n2. Eventos online"}

    # Handling of first question
    if conversation_state["last_question"] == "tipo_evento":
        if "eventos presenciales" in user_query:
            conversation_state["last_question"] = "evento_presencial_mes"
            return {"response": "¿Quieres ver los eventos locales del mes actual o de algún otro mes?"}
        elif "eventos online" in user_query:
            from .routes import get_online_events
            events = get_online_events()
            conversation_state["last_question"] = None  # Reset status after this response
            if events:
                return {"response": f"Aquí tienes los eventos online disponibles. Si quieres ver más detalles del evento puedes entrar al link!!\n{events}"}
            else:
                return {"response": "No hay eventos online disponibles por el momento, pero puedes intentar luego y ver si hay novedades."}
        else:
            # If the answer is not valid, repeat the question
            return {"response": "¿Qué tipo de eventos te gustaría conocer?\n1. Eventos presenciales\n2. Eventos online"}

    # Handling of the response to the question about on-site events
    if conversation_state["last_question"] == "evento_presencial_mes":
        if "mes actual" in user_query:
            from .routes import events_this_month
            events = events_this_month()
            if events:
                response = f"Con gusto te mostraré los eventos de interés de este mes:\n{events}\n¿Te gustaría ver eventos de otro mes?"
            else:
                response = "No hay eventos disponibles para este mes por el momento, pero puedes intentar luego y ver si hay novedades.\n¿Te gustaría ver eventos de otro mes? Responde con 'sí' o 'no'."
            conversation_state["last_question"] = "preguntar_otro_mes"
            return {"response": response}

        # Specific month query
        elif any(month in user_query for month in ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "setiembre", "octubre", "noviembre", "diciembre"]):
            from .routes import extract_month_from_query, get_events_by_specific_month
            month = extract_month_from_query(user_query)
            if month:
                events = get_events_by_specific_month(month)
                if events:
                    response = f"Claro, te mostraré los eventos de {month}:\n{events}\n¿Te gustaría ver eventos de otro mes?"
                else:
                    response = f"No hay eventos disponibles para el mes {month}, pero puedes intentar luego y ver si hay novedades.\n¿Te gustaría ver eventos de otro mes? Responde con 'sí' o 'no'."
                conversation_state["last_question"] = "preguntar_otro_mes"
                return {"response": response}
            return {"response": "No entendí qué mes quieres consultar. ¿Podrías ser más específico?"}
        
        else:
            # If the answer is not valid, repeat the question
            return {"response": "¿Quieres ver los eventos locales del mes actual o de algún otro mes?"}

    # Handling of asking for another month
    if conversation_state["last_question"] == "preguntar_otro_mes":
        if "si" in user_query or "sí" in user_query:
            conversation_state["last_question"] = "evento_presencial_mes"
            return {"response": "¿Qué mes te gustaría consultar?"}
        elif "no" in user_query:
            conversation_state["last_question"] = "tipo_evento"
            return {"response": "¡Entendido! ¿Qué tipo de eventos te gustaría conocer?\n1. Eventos presenciales\n2. Eventos online"}
        else:
            return {"response": "¿Te gustaría ver eventos de otro mes? Responde con 'sí' o 'no'."}

    # Default response for unrecognized entries
    return {"response": "Lo siento, no entendí tu pregunta. ¿Podrías ser más específico?"}
