import json

# Global variable for storing the status of the conversation
conversation_state = {"last_question": None}

def chat(query):
    global conversation_state
    user_query = query.lower()

    # Check if user wants to start over
    if user_query == "exit":
        conversation_state["last_question"] = "tipo_evento"
        return {"response": "¡Has vuelto al inicio! ¿Qué tipo de eventos te gustaría conocer?\n1. Eventos presenciales\n2. Eventos online"}

    # Initial greeting and first question
    if conversation_state["last_question"] is None:
        if user_query in ["hola", "hi", "buenos días", "buenas tardes", "buenas noches"]:
            conversation_state["last_question"] = "tipo_evento"
            return {"response": "¡Hola! Soy tu chatbot de eventos. ¿Qué tipo de eventos te gustaría conocer?\n1. Eventos presenciales\n2. Eventos online"}

    # Handling of first question
    if conversation_state["last_question"] == "tipo_evento":
        if "eventos presenciales" in user_query:
            conversation_state["last_question"] = "evento_presencial_mes"
            return {"response": "¿Quieres ver los eventos locales del mes actual o de algún otro mes?\nPuedes escribir 'exit' para volver al inicio."}
        elif "eventos online" in user_query:
            from .routes import get_online_events
            events = get_online_events()
            conversation_state["last_question"] = "preguntar_evento_presencial"
            if events:
                response = {
                    "message": "Aquí están los eventos online disponibles. Si deseas más detalles, puedes entrar al link.",
                    "events": events,
                    "query_next_month": "¿Te gustaría ver eventos presenciales también? Responde 'sí' o 'no'.",
                    "exit_message": "Puedes escribir 'exit' para volver al inicio."
                }
                return response
            else:
                return {"response": "No hay eventos online disponibles por el momento, pero puedes intentar luego y ver si hay novedades.\n¿Te gustaría consultar eventos presenciales también? Responde con 'sí' o 'no'.\nPuedes escribir 'exit' para volver al inicio."}
        else:
            # If the answer is not valid, repeat the question
            return {"response": "¿Qué tipo de eventos te gustaría conocer?\n1. Eventos presenciales\n2. Eventos online"}

    # Handling of the response to the question about on-site events
    if conversation_state["last_question"] == "evento_presencial_mes":
        if "mes actual" in user_query:
            from .routes import events_this_month
            events = events_this_month()
            if events:
                response = {
                    "message": "Claro, te mostraré los eventos de interés de este mes:",
                    "events": events,
                    "query_next_month": "¿Te gustaría ver eventos de otro mes? Responde 'sí' o 'no'.",
                    "exit_message": "Puedes escribir 'exit' para volver al inicio."
                }
                return response
            else:
                response = {
                    "response": "No hay eventos disponibles para este mes por el momento, pero puedes intentar luego y ver si hay novedades. ¿Te gustaría ver eventos de otro mes? Responde con 'sí' o 'no'. Puedes escribir 'exit' para volver al inicio."
                }
            conversation_state["last_question"] = "preguntar_otro_mes"
            return response

        # Specific month query
        elif any(month in user_query for month in ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "setiembre", "octubre", "noviembre", "diciembre"]):
            from .routes import extract_month_from_query, get_events_by_specific_month
            month = extract_month_from_query(user_query)
            if month:
                events = get_events_by_specific_month(month)
                if events:
                    response = {
                        "message": "Claro, te mostraré los eventos:",
                        "month": month,
                        "events": events,
                        "query_next_month_and_exit": "¿Te gustaría ver eventos de otro mes? Puedes escribir 'exit' para volver al inicio."
                    }
                else:
                    response = {
                        "message": "No hay eventos disponibles para el mes",
                        "month": month, 
                        "text":" pero puedes intentar luego y ver si hay novedades!!!.",
                        "query_next_month_and_exit": "¿Te gustaría ver eventos de otro mes? Responde con 'sí' o 'no'. Puedes escribir 'exit' para volver al inicio."
                    }
                conversation_state["last_question"] = "preguntar_otro_mes"
                return response
            return {"response": "No entendí qué mes quieres consultar. ¿Podrías ser más específico?\nPuedes escribir 'exit' para volver al inicio."}

        else:
            # If the answer is not valid, repeat the question
            return {"response": "¿Quieres ver los eventos locales del mes actual o de algún otro mes?\nPuedes escribir 'exit' para volver al inicio."}

    # Handling of asking for another month
    if conversation_state["last_question"] == "preguntar_otro_mes":
        if "si" in user_query or "sí" in user_query:
            conversation_state["last_question"] = "evento_presencial_mes"
            return {"response": "¿Qué mes te gustaría consultar?\nPuedes escribir 'exit' para volver al inicio."}

        elif "no" in user_query:
            conversation_state["last_question"] = "tipo_evento"
            return {"response": "¡Entendido! ¿Qué tipo de eventos te gustaría conocer?\n1. Eventos presenciales\n2. Eventos online\nPuedes escribir 'exit' para volver al inicio."}

        else:
            return {"response": "¿Te gustaría ver eventos de otro mes? Responde con 'sí' o 'no'.\nPuedes escribir 'exit' en cualquier momento para volver al inicio."}

    # Handling of asking about on-site events after online events
    if conversation_state["last_question"] == "preguntar_evento_presencial":
        if "si" in user_query or "si" in user_query:
            conversation_state["last_question"] = "evento_presencial_mes"
            return {"response": "¿Quieres ver los eventos locales del mes actual o de algún otro mes?\nPuedes escribir 'exit' en cualquier momento para volver al inicio."}
        elif "no" in user_query:
            conversation_state["last_question"] = "tipo_evento"
            return {"response": "¡Entendido! ¿Qué tipo de eventos te gustaría conocer?\n1. Eventos presenciales\n2. Eventos online\nPuedes escribir 'exit' en cualquier momento para volver al inicio."}
        else:
            return {"response": "¿Te gustaría consultar eventos presenciales también? Responde con 'sí' o 'no'.\nPuedes escribir 'exit' en cualquier momento para volver al inicio."}

    # Default response for unrecognized entries
    return {"response": "Lo siento, no entendí tu pregunta.\nPuedes escribir 'exit' en cualquier momento para volver al inicio."}
