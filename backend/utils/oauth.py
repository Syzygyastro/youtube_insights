# utils/oauth.py
import os
import pathlib
from flask import session, url_for, redirect
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# Path to the client secret JSON file
CLIENT_SECRETS_FILE = os.path.join(pathlib.Path(__file__).parent.absolute(), "client_secret.json")

# Scopes required for accessing YouTube data
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

def get_flow():
    return Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('auth.oauth2callback', _external=True)
    )

def is_authenticated():
    return 'credentials' in session

def get_credentials():
    if not is_authenticated():
        return None
    credentials = Credentials(**session['credentials'])
    # Refresh the token if it's expired
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        session['credentials'] = credentials_to_dict(credentials)
    return credentials

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
