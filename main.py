#!/usr/bin/python3

import auth
import calendar_api
import datetime
import json

from flask import Flask, Response

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, world!'


@app.route('/events')
def events():
    service = auth.get_calendar_service()
    now = (datetime.datetime.utcnow()-datetime.timedelta(hours=1)).isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events, time_zone = calendar_api.get_events(
        service, end_cap=now, max_results=100)

    json_dict = {'timeZone': time_zone,
                 'events': [calendar_api.parse_event_info(e) for e in events]}
    return json.dumps(json_dict)


@app.route('/download_ics/<event_id>', methods=['GET'])
def download_ics(event_id):
    service = auth.get_calendar_service()
    ics = calendar_api.get_event_ics(service, event_id)
    return Response(
        str(ics),
        headers={"Content-disposition":
                 "attachment; filename=event.ics"})
