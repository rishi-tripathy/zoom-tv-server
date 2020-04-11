"""
API for Google Calendar functions.
"""


def get_events(service, start_time, max_results):
    events_result = service.events().list(
        calendarId='primary', timeMin=start_time, maxResults=max_results,
        singleEvents=True, orderBy='startTime').execute()
    print(events_result)
    events = events_result.get('items', [])
    time_zone = events_result['timeZone']
    return events, time_zone
