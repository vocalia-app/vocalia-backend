from flask import Flask, request, jsonify
import os
from calendar_utils import get_availability, create_event
from twilio_utils import send_whatsapp

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Vocalia backend OK"

@app.route('/disponibilidad', methods=['GET'])
def disponibilidad():
    fecha = request.args.get('fecha')  # expected YYYY-MM-DD
    calendar_id = request.args.get('calendar_id') or os.environ.get('DEFAULT_CALENDAR_ID')
    if not fecha:
        return jsonify({'error': 'Parámetro fecha requerido (YYYY-MM-DD)'}), 400
    try:
        slots = get_availability(calendar_id, fecha)
        return jsonify({'fecha': fecha, 'slots': slots})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reservar', methods=['POST'])
def reservar():
    data = request.get_json(force=True)
    nombre = data.get('nombre') or data.get('name')
    fecha = data.get('fecha')
    hora = data.get('hora')
    telefono = data.get('telefono') or data.get('phone')
    calendar_id = data.get('calendar_id') or os.environ.get('DEFAULT_CALENDAR_ID')

    if not all([nombre, fecha, hora, telefono]):
        return jsonify({'error': 'nombre, fecha, hora y telefono son requeridos'}), 400

    try:
        event = create_event(calendar_id, nombre, fecha, hora)
        # Send confirmation WhatsApp
        msg = f"Hola {nombre}, tu cita ha sido confirmada para el {fecha} a las {hora}."
        send_whatsapp(telefono, msg)
        return jsonify({'status': 'ok', 'eventId': event.get('id')}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
