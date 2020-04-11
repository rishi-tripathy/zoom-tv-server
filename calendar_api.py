"""
API for Google Calendar functions.
"""
import ics


# TODO: zoom link.
def parse_event_info(event):
    return {'id': event['id'],
            'summary': event['summary'],
            'start': event['start'].get('dateTime',
                                        event['start'].get('date')),
            'end': event['end'].get('dateTime', event['end'].get('date')),
            'creator': event['creator']['email'],
            'description': event.get('description')}


def get_events(service, start_time, max_results):
    """Gets multiple events."""
    events_result = service.events().list(
        calendarId='primary', timeMin=start_time, maxResults=max_results,
        singleEvents=True, orderBy='startTime').execute()
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
