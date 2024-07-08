# Variable global para almacenar el estado de la conversación
conversation_state = {"last_question": None}

def chat(query):
    global conversation_state
    user_query = query.lower()

    # Saludo inicial y primer pregunta
    if conversation_state["last_question"] is None:
        if user_query in ["hola", "hi", "buenos días", "buenas tardes", "buenas noches"]:
            conversation_state["last_question"] = "tipo_evento"
            return {"response": "¡Hola! Soy tu chatbot de eventos. ¿Qué tipo de eventos te gustaría conocer?\n1. Eventos presenciales\n2. Eventos online"}

    # Manejo de respuesta a la primera pregunta
    if conversation_state["last_question"] == "tipo_evento":
        if "eventos presenciales" in user_query:
            conversation_state["last_question"] = "evento_presencial_mes"
            return {"response": "¿Quieres ver los eventos locales del mes actual o de algún otro mes?"}
        elif "eventos online" in user_query:
            conversation_state["last_question"] = None  # Resetear el estado después de esta respuesta
            return {"response": "Aquí tienes los eventos online disponibles. ¿Te gustaría ver más detalles sobre alguno en particular?"}
        else:
            # Si la respuesta no es válida, repetir la pregunta
            return {"response": "¿Qué tipo de eventos te gustaría conocer?\n1. Eventos presenciales\n2. Eventos online"}

    # Manejo de respuesta a la pregunta sobre eventos presenciales
    if conversation_state["last_question"] == "evento_presencial_mes":
        if "mes actual" in user_query or "otro mes" in user_query:
            from .routes import events_this_month
            events = events_this_month()
            conversation_state["last_question"] = None  # Resetear el estado después de esta respuesta
            if events:
                return {"response": f"Con gusto te mostraré los eventos de interés de este mes:\n{events}"}
            else:
                return {"response": "No hay eventos disponibles para este mes por el momento, pero puedes intentar luego y ver si hay novedades."}
        else:
            # Si la respuesta no es válida, repetir la pregunta
            return {"response": "¿Quieres ver los eventos locales del mes actual o de algún otro mes?"}

    # Respuesta por defecto para entradas no reconocidas
    return {"response": "Lo siento, no entendí tu pregunta. ¿Podrías ser más específico?"}


