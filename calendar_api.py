"""
API for Google Calendar functions.
"""
import ics
import re


def parse_event_info(event):
    return {'id': event['id'],
            'summary': event['summary'],
            'start': event['start'].get('dateTime',
                                        event['start'].get('date')),
            'end': event['end'].get('dateTime', event['end'].get('date')),
            'creator': event['creator']['email'],
            'description': get_event_description(event),
            'tags': get_event_tags(event),
            'zoom': get_zoom_link(event),
            'recurrence': event.get('recurrence')
            }


def get_events(service, end_cap, max_results):
    """Gets multiple events."""
    events_result = service.events().list(
        calendarId='primary', timeMin=end_cap, maxResults=max_results,
        singleEvents=False).execute()
    events = events_result.get('items', [])
    time_zone = events_result['timeZone']
    return events, time_zone


def get_event(service, event_id):
    event = service.events().get(
        calendarId='primary', eventId=event_id).execute()
    return event


def get_event_ics(service, event_id):
    event = get_event(service, event_id)
    calendar = ics.Calendar()
    event_info = parse_event_info(event)

    event = ics.Event(
        name=event_info['summary'], begin=event_info['start'],
        description=event_info['description'],
        end=event_info['end'], organizer=event_info['creator'])

    calendar.events.add(event)
    return calendar


def get_event_tags(event):
    desc = event.get('description')
    if desc:
        tags = re.findall(r'#\w+', desc)
        return [str(tag)[1:] for tag in tags]
    return []


def get_event_description(event):
    desc = event.get('description')
    if desc:
        m = re.search(r'^[\S\s]*?(?=(─|$))', desc)
        if m:
            match = m.group(0)
            match = match.replace("<br>", " ")
            match = match.replace("\\n", " ")
            return match
    return ""


def get_zoom_link(event):
    desc = event.get('description')
    if desc:
        dm = re.search(r'https.*?($|\")', desc)
        if dm:
            return dm.group(0)
    loc = event.get('location')
    if loc:
        lm = re.search(r'https.*?($|\")', loc)
        if lm:
            return lm.group(0)
    return ""


def delete_event(service, event_id):
    service.events().delete(calendarId='primary', eventId=event_id).execute()
