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

def get_popular_channels_by_topic(topic_names, subscribed_channel_ids):
    youtube = get_youtube_client()
    if not youtube:
        return None

    recommended_channels = []
    seen_channel_ids = set(subscribed_channel_ids)

    for topic_name in topic_names:
        # Use the topic name as a keyword
        keyword = topic_name
        print(keyword)
        request = youtube.search().list(
            part='snippet',
            type='channel',
            q=keyword,
            maxResults=20,
            order='relevance'
        )
        response = request.execute()
        for item in response.get('items', []):
            channel_id = item['snippet']['channelId']
            if channel_id not in seen_channel_ids:
                seen_channel_ids.add(channel_id)
                # Fetch channel details
                channel_request = youtube.channels().list(
                    part='snippet,statistics',
                    id=channel_id
                )
                channel_response = channel_request.execute()
                channel_items = channel_response.get('items', [])
                if channel_items:
                    channel_info = channel_items[0]
                    subscriber_count = int(channel_info['statistics'].get('subscriberCount', 0))
                    recommended_channels.append({
                        'channelId': channel_id,
                        'title': channel_info['snippet']['title'],
                        'description': channel_info['snippet']['description'],
                        'thumbnails': channel_info['snippet']['thumbnails'],
                        'subscriberCount': subscriber_count
                    })

    # Sort channels by subscriber count
    recommended_channels.sort(key=lambda x: x['subscriberCount'], reverse=True)
    return recommended_channels[:10]