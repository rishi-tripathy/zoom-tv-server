#!/usr/bin/python3

import auth
import calendar_api
import datetime
import json

from flask import Flask

app = Flask(__name__)


# TODO: zoom link.
def parse_event_info(event):
    return {'id': event['id'],
            'summary': event['summary'],
            'start': event['start'].get('dateTime',
                                        event['start'].get('date')),
            'creator': event['creator']['email'],
            'description': event.get('description')}


@app.route('/')
def hello_world():
    return 'Hello, world!'


@app.route('/events')
def events():
    service = auth.get_calendar_service()
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events, time_zone = calendar_api.get_events(
        service, start_time=now, max_results=100)

    json_dict = {'timeZone': time_zone,
                 'events': [parse_event_info(e) for e in events]}
    return json.dumps(json_dict)
