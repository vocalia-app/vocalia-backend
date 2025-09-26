# Vocalia - Flask starter

Proyecto mínimo para el backend de Vocalia: endpoints para comprobar disponibilidad y reservar citas,
integrando Google Calendar y Twilio (WhatsApp).

## Archivos principales
- `app.py` - Flask app con endpoints `/disponibilidad` y `/reservar`.
- `calendar_utils.py` - funciones para listar eventos y crear citas usando Google Calendar API.
- `twilio_utils.py` - función para enviar WhatsApp con Twilio.
- `requirements.txt` - dependencias.

## Variables de entorno (requeridas)
- `GOOGLE_APPLICATION_CREDENTIALS` -> ruta al `credentials.json` de la cuenta de servicio.
- `DEFAULT_CALENDAR_ID` -> ID del calendario donde se crearán eventos.
- `TWILIO_SID` -> Twilio Account SID.
- `TWILIO_AUTH_TOKEN` -> Twilio Auth Token.
- `TWILIO_WHATSAPP_FROM` -> Ej: 'whatsapp:+14155238886'

## Ejecutar localmente
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
export DEFAULT_CALENDAR_ID="your_calendar_id"
export TWILIO_SID="ACxxxxx"
export TWILIO_AUTH_TOKEN="yourtoken"
export TWILIO_WHATSAPP_FROM="whatsapp:+14155238886"
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
```

## Pruebas (ejemplos)
- Comprobar disponibilidad:
```
curl 'http://localhost:5000/disponibilidad?fecha=2025-10-01'
```
- Reservar (JSON POST):
```
curl -X POST http://localhost:5000/reservar -H "Content-Type: application/json" \
  -d '{"nombre":"Carlos","fecha":"2025-10-01","hora":"13:00","telefono":"+34XXXXXXXXX"}'
```

## Despliegue en Render
1. Sube este repositorio a GitHub.
2. Crea un nuevo **Web Service** en Render y conecta tu repo.
3. En "Environment" añade las variables de entorno indicadas arriba.
4. Start command: `gunicorn app:app`
