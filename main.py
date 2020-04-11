#!/usr/bin/python3

import auth
import datetime
import quickstart

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, world! Testing CloudBuild'


@app.route('/events')
def events():
    service = auth.get_calendar_service()
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    """
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    """
    return events[0]['summary']
