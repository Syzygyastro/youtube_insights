# controllers/data_controller.py
from flask import Blueprint, jsonify, redirect, render_template, url_for
from services.youtube_service import get_user_subscriptions
from services.analysis_service import analyze_subscriptions
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
