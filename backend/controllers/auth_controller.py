from flask import Blueprint, session, redirect, url_for, request, flash
from utils.oauth import get_flow, is_authenticated, credentials_to_dict

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    flow = get_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    session['state'] = state
    return redirect(authorization_url)

@auth_bp.route('/oauth2callback')
def oauth2callback():
    flow = get_flow()
    flow.fetch_token(authorization_response=request.url)

    if not flow.credentials:
        flash('Authentication failed.')
        return redirect(url_for('index'))

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('data.dashboard'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('index'))
