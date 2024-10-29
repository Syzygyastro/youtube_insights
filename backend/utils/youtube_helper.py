# utils/youtube_helper.py

from googleapiclient.discovery import build
from utils.oauth import get_credentials

def get_youtube_client():
    credentials = get_credentials()
    if not credentials:
        return None
    return build('youtube', 'v3', credentials=credentials)
