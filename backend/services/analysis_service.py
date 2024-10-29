# services/analysis_service.py

from utils.youtube_helper import get_youtube_client
from collections import defaultdict
import urllib.parse

def analyze_subscriptions(subscriptions):
    youtube = get_youtube_client()
    if not youtube:
        return None

    channel_ids = [item['snippet']['resourceId']['channelId'] for item in subscriptions]

    def chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    category_count = defaultdict(int)
    for chunk in chunks(channel_ids, 50):
        request = youtube.channels().list(
            part='snippet,topicDetails',
            id=','.join(chunk)
        )
        response = request.execute()
        for item in response.get('items', []):
            topics = item.get('topicDetails', {}).get('topicCategories', [])
            channel_title = item['snippet']['title']
            if topics:
                for topic_url in topics:
                    # Extract the topic name from the URL
                    topic_name = urllib.parse.unquote(topic_url.split('/')[-1]).replace('_', ' ')
                    category_count[topic_name] += 1
            else:
                category_count['Uncategorized'] += 1
    return category_count
