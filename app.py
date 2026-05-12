import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN_VERIFICACION = os.environ.get("VERIFY_TOKEN", "mi_token_secreto_123")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
ID_TELEFONO = os.environ.get("PHONE_NUMBER_ID")

@app.route('/webhook', methods=['GET'])
def verificar_webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if mode == 'subscribe' and token == TOKEN_VERIFICACION:
        return challenge, 200
    return 'Error', 403

@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    try:
        body = request.get_json()
        value = body['entry'][0]['changes'][0]['value']
        if 'messages' in value:
            mensaje = value['messages'][0]['text']['body'].lower()
            numero = value['messages'][0]['from']
            respuesta = "¡Hola! ¿En qué podemos ayudarte?"
            if "precio" in mensaje:
                respuesta = "Nuestros precios son competitivos. ¡Pregúntanos!"
            enviar_mensaje_whatsapp(numero, respuesta)
        return jsonify({"status": "success"}), 200
    except:
        return jsonify({"status": "error"}), 500

def enviar_mensaje_whatsapp(numero, texto):
    url = f"https://graph.facebook.com/v18.0/{ID_TELEFONO}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp", "to": numero, "type": "text", "text": {"body": texto}}
    requests.post(url, headers=headers, json=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
