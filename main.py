#!/usr/bin/python3

import auth
import calendar_api
import datetime
import json
import os

from flask import Flask, Response, request
import flask_mail

app = Flask(__name__)

app.config.update(
    DEBUG=True,
    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'))


@app.route('/')
def hello_world():
    return 'Hello, world!'


@app.route('/events', methods=['GET'])
def events():
    service = auth.get_calendar_service()
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events, time_zone = calendar_api.get_events(
        service, start_time=now, max_results=100)

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


@app.route('/report', methods=['POST'])
def report():
    print(os.environ.get('MAIL_USERNAME'))
    print(os.environ.get('MAIL_PASSWORD'))
    req_json = request.get_json()
    event_id = req_json.get('eventId')
    # Send email
    mail = flask_mail.Mail(app)
    message = flask_mail.Message(
        subject='Zoom Event Reported',
        body='Event ID: %s' % event_id,
        recipients='zoom.tv.guide@gmail.com')
    mail.send(message)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
