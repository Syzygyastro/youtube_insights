# services/analysis_service.py
def analyze_subscriptions(subscriptions):
    category_count = {}
    for sub in subscriptions:
        title = sub['snippet']['title']
        # Simple keyword-based categorization
        if 'Music' in title:
            category = 'Music'
        elif 'Game' in title:
            category = 'Gaming'
        elif 'News' in title:
            category = 'News'
        else:
            category = 'Others'
        category_count[category] = category_count.get(category, 0) + 1
    return category_count
