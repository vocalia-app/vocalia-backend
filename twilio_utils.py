import os
from twilio.rest import Client

TWILIO_SID = os.environ.get('TWILIO_SID')
TWILIO_AUTH = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_FROM = os.environ.get('TWILIO_WHATSAPP_FROM')  # e.g. 'whatsapp:+14155238886'

client = None
if all([TWILIO_SID, TWILIO_AUTH, TWILIO_WHATSAPP_FROM]):
    client = Client(TWILIO_SID, TWILIO_AUTH)

def send_whatsapp(to_number, body):
    if client is None:
        raise RuntimeError('Twilio no está configurado. Define TWILIO_SID, TWILIO_AUTH_TOKEN y TWILIO_WHATSAPP_FROM')
    to = to_number if to_number.startswith('whatsapp:') else f'whatsapp:{to_number}'
    message = client.messages.create(from_=TWILIO_WHATSAPP_FROM, body=body, to=to)
    return message.sid
