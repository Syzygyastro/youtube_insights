# services/youtube_service.py

from utils.youtube_helper import get_youtube_client

def get_user_subscriptions():
    youtube = get_youtube_client()
    if not youtube:
        return None
    subscriptions = []
    request = youtube.subscriptions().list(
        part='snippet,contentDetails',
        mine=True,
        maxResults=50
    )
    while request is not None:
        response = request.execute()
        subscriptions.extend(response.get('items', []))
        request = youtube.subscriptions().list_next(request, response)
    return subscriptions
