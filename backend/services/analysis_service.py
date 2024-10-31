# services/analysis_service.py

from utils.youtube_helper import get_youtube_client
from collections import defaultdict
import urllib.parse
import re

def analyze_subscriptions(subscriptions):
    youtube = get_youtube_client()
    if not youtube:
        return None

    channel_ids = [item['snippet']['resourceId']['channelId'] for item in subscriptions]

    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    category_count = defaultdict(int)
    topic_id_count = defaultdict(int)
    topic_id_to_name = {}

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
                    # Extract the topic name from the Wikipedia URL
                    parsed_url = urllib.parse.urlparse(topic_url)
                    topic_name_raw = parsed_url.path.split('/')[-1]
                    topic_name = urllib.parse.unquote(topic_name_raw).replace('_', ' ')
                    # Clean up the topic name
                    topic_name_clean = re.sub(r'\(.*\)', '', topic_name).strip()

                    # Update counts using topic_name_clean
                    category_count[topic_name_clean] += 1

                    topic_id = topic_name_clean

                    topic_id_count[topic_id] += 1
                    topic_id_to_name[topic_id] = topic_name_clean
            else:
                category_count['Uncategorized'] += 1
                topic_id_count['Uncategorized'] += 1
                topic_id_to_name['Uncategorized'] = 'Uncategorized'

    return {
        'category_count': dict(category_count),
        'topic_id_count': dict(topic_id_count),
        'topic_id_to_name': topic_id_to_name
    }
