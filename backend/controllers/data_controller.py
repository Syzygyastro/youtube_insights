# controllers/data_controller.py
from flask import Blueprint, jsonify, redirect, render_template, url_for
from services.youtube_service import get_user_subscriptions
from services.analysis_service import analyze_subscriptions
from services.youtube_service import get_popular_channels_by_topic
from utils.oauth import is_authenticated

data_bp = Blueprint('data', __name__)

@data_bp.route('/dashboard')
def dashboard():
    if not is_authenticated():
        return redirect(url_for('auth.login'))
    subscriptions = get_user_subscriptions()
    analysis = analyze_subscriptions(subscriptions)
    return render_template('dashboard.html', analysis=analysis, subscriptions=subscriptions)

@data_bp.route('/api/subscriptions')
def api_subscriptions():
    if not is_authenticated():
        return redirect(url_for('auth.login'))
    subscriptions = get_user_subscriptions()
    if subscriptions is None:
        return jsonify({'error': 'Unable to fetch subscriptions'}), 500
    return jsonify(subscriptions)

@data_bp.route('/api/analysis')
def api_analysis():
    if not is_authenticated():
        return jsonify({'error': 'User not authenticated'}), 401
    subscriptions = get_user_subscriptions()
    if subscriptions is None:
        return jsonify({'error': 'Unable to fetch subscriptions'}), 500
    analysis = analyze_subscriptions(subscriptions)
    return jsonify(analysis)


@data_bp.route('/api/recommendations')
def api_recommendations():
    if not is_authenticated():
        return jsonify({'error': 'User not authenticated'}), 401

    subscriptions = get_user_subscriptions()
    if subscriptions is None:
        return jsonify({'error': 'Unable to fetch subscriptions'}), 500

    subscribed_channel_ids = [item['snippet']['resourceId']['channelId'] for item in subscriptions]

    # Analyze subscriptions to get topic IDs
    analysis = analyze_subscriptions(subscriptions)
    topic_id_count = analysis['topic_id_count']
    topic_id_to_name = analysis['topic_id_to_name']

    # Sort topics by frequency
    sorted_topics = sorted(topic_id_count.items(), key=lambda x: x[1], reverse=True)
    top_topic_ids = [topic_id for topic_id, count in sorted_topics[:3]]  # Top 3 topics
    
    top_topic_names = [topic_id_to_name[topic_id] for topic_id in top_topic_ids]

    # Get recommended channels
    recommended_channels = get_popular_channels_by_topic(top_topic_names, subscribed_channel_ids)

    return jsonify(recommended_channels)