import os
from datetime import datetime, time as dtime
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

SERVICE_ACCOUNT_FILE = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 'credentials.json')
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=creds)

def _list_events(calendar_id, time_min, time_max):
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=time_min.isoformat(),
        timeMax=time_max.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])

def get_availability(calendar_id, date_str):
    tz = pytz.timezone('Europe/Madrid')
    date_dt = datetime.strptime(date_str, '%Y-%m-%d').date()
    start_dt = tz.localize(datetime.combine(date_dt, dtime(9, 0)))
    end_dt = tz.localize(datetime.combine(date_dt, dtime(19, 0)))
    events = _list_events(calendar_id, start_dt, end_dt)

    busy_hours = set()
    for e in events:
        s = e['start'].get('dateTime') or e['start'].get('date')
        if 'T' in s:
            start = datetime.fromisoformat(s.replace('Z', '+00:00'))
            start = start.astimezone(tz)
            busy_hours.add(start.hour)

    slots = []
    for h in range(9, 19):
        if h not in busy_hours:
            slots.append(f"{h:02d}:00")
    return slots

def create_event(calendar_id, name, date_str, hour_str, duration_minutes=60):
    tz = 'Europe/Madrid'
    hour = hour_str.split(':')[0]
    hour_int = int(hour)
    start_iso = f"{date_str}T{hour_int:02d}:00:00"
    end_hour = hour_int + (duration_minutes // 60)
    end_iso = f"{date_str}T{end_hour:02d}:00:00"

    event = {
        'summary': f'Cita con {name}',
        'start': {'dateTime': start_iso, 'timeZone': tz},
        'end': {'dateTime': end_iso, 'timeZone': tz},
    }
    created = service.events().insert(calendarId=calendar_id, body=event).execute()
    return created
