#!/usr/bin/python3

import auth
import calendar_api
import datetime
import json
from flask import Flask, Response, render_template, request
import flask_mail

SUCCESS_STATUS = json.dumps({'success': True}), 200, {
    'ContentType': 'application/json'
}

app = Flask(__name__)

mail_username, mail_password = auth.mail_creds()
app.config.update(
    DEBUG=True,
    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_DEFAULT_SENDER='zoom.tv.guide@gmail.com',
    MAIL_USERNAME=mail_username,
    MAIL_PASSWORD=mail_password)
mail = flask_mail.Mail(app)


@app.route('/')
def hello_world():
    return 'Hello, world!'


@app.route('/events', methods=['GET'])
def events():
    service = auth.get_calendar_service()
    now = (datetime.datetime.utcnow()-datetime.timedelta(hours=1)
           ).isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events, time_zone = calendar_api.get_events(
        service, end_cap=now, max_results=100)
    json_dict = {'timeZone': time_zone,
                 'events': [calendar_api.parse_event_info(e) for e in events]}
    for e in json_dict.get('events'):
        if e.get('zoom') == "":
            # No zoom link found, send email
            message = flask_mail.Message(
                subject='No Link included in your ZoomTV Event',
                body="Your ZoomTV event titled {} doesn't seem to have a Zoom link in the location or description. \
                Please add one so people can find your event!".format(e.get('summary')),
                recipients=[str(e['creator'])])
            mail.send(message)
    dump = json.dumps(json_dict)
    resp = Response(dump)
    resp.headers["Access-Control-Allow-Origin"] = '*'
    return resp


@app.route('/download_ics/<event_id>', methods=['GET'])
def download_ics(event_id):
    service = auth.get_calendar_service()
    ics = calendar_api.get_event_ics(service, event_id)
    return Response(
        str(ics),
        headers={"Access-Control-Allow-Origin": "*",
                 "Content-disposition":
                 "attachment; filename=event.ics"})


@app.route('/report', methods=['POST'])
def report():
    service = auth.get_calendar_service()
    req_json = request.get_json()
    event_id = req_json.get('eventId')
    # Send email
    event = calendar_api.get_event(service, event_id)
    event_info = calendar_api.parse_event_info(event)
    mail = flask_mail.Mail(app)
    message = flask_mail.Message(
        subject='Zoom Event Reported',
        html=render_template('report_event.html', **event_info),
        recipients=['zoom.tv.guide@gmail.com'])
    mail.send(message)
    return SUCCESS_STATUS


@app.route('/delete_zoom', methods=['POST'])
def delete_event():
    """Removes calendar event with specified eventId."""
    service = auth.get_calendar_service()
    event_id = request.form.get('event_id')
    event = calendar_api.get_event(service, event_id)
    event_info = calendar_api.parse_event_info(event)
    calendar_api.delete_event(service, event_id)

    # Send email to whoever's event it was notifying them.
    mail = flask_mail.Mail(app)
    message = flask_mail.Message(
        subject='Your Zoom Event was Removed',
        html=render_template('removed_event.html', **event_info),
        recipients=[event_info['creator']])
    mail.send(message)

    return "Event %s with ID %s was successfully removed." % (
        event_info['summary'], event_id)
