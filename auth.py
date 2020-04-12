import json
import os
import os.path
from google.oauth2 import service_account

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.cloud import datastore

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SERVICE_ACCOUNT_FILE = 'secrets/token.json'


def calendar_service_creds():
    """Gets the host, username, and password from Datastore."""
    # Get auth variables from cloud datastore.
    datastore_client = datastore.Client()
    query = datastore_client.query(kind='GaeEnvSettings')
    env_vars = list(query.fetch())[0]
    token = json.loads(env_vars['TOKEN_JSON'])
    return service_account.Credentials.from_service_account_info(
        token
    )
    """
    except:
        return service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
    """


def mail_creds():
    """Gets the host, username, and password from Datastore."""
    try:
        # Get auth variables from cloud datastore.
        datastore_client = datastore.Client()
        query = datastore_client.query(kind='GaeEnvSettings')
        env_vars = list(query.fetch())[0]
        return env_vars['MAIL_USERNAME'], env_vars['MAIL_PASSWORD']
    except:
        return os.environ.get('MAIL_USERNAME'), os.environ.get('MAIL_PASSWORD')


def get_calendar_service():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    service = build('calendar', 'v3', credentials=calendar_service_creds())
    return service
