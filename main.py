#!/usr/bin/python3

import auth
import calendar_api
import datetime

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, world!'


@app.route('/events')
def events():
    service = auth.get_calendar_service()
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events = calendar_api.get_events(service, start_time=now, max_results=10)

    if not events:
        return 'No upcoming events found.'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))

    return str([e['summary'] for e in events])
