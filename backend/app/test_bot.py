import json
import requests

# URL de tu servidor FastAPI donde está alojado el chatbot
url = "http://127.0.0.1:8000/chat"  # Actualiza con tu propia URL

# Función para interactuar con el chatbot
def interact_with_chatbot():
    print("¡Bienvenido al chatbot de eventos!")
    print("Escribe 'salir' para terminar la conversación.\n")

    while True:
        user_input = input("Tú: ")

        if user_input.lower() == "salir":
            print("Hasta luego!")
            break

        # Enviar la solicitud al chatbot
        response = send_message_to_chatbot(user_input)

        if 'response' in response:
            print(f"Chatbot: {response['response']}\n")
        elif 'message' in response:
            print(f"Chatbot: {response['message']}\n")
            if 'events' in response:
                print("Eventos Disponibles:")
                for event in response['events']:
                    print(f"- Nombre: {event['name']}")
                    print(f"  Descripción: {event['description']}")
                    print(f"  Inicia: {event['start']} - Termina: {event['end']}")
                    print(f"  URL: {event['url']}")
                    print()
                print(response.get('query_next_month', ''))
                print(response.get('exit_message', ''))
        else:
            print(f"Chatbot: Respuesta no reconocida del servidor.\n")

def send_message_to_chatbot(message):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "query": message
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return {"response": f"Error: {response.status_code}, {response.text}"}

# Ejecutar la función de interacción
if __name__ == "__main__":
    interact_with_chatbot()
