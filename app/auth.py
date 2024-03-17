from flask import Blueprint, session, request, redirect, url_for, flash, current_app
import os
import uuid
import requests
from base64 import b64encode
import time
from .spotify import get_spotify_auth_url, exchange_code_for_token, get_saved_tracks, refresh_access_token


auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login')
def login():
    state = str(uuid.uuid4())
    session['state'] = state

    auth_url = get_spotify_auth_url(scopes=[current_app.config['SPOTIFY_SCOPE']])  # Use the config variable
    return redirect(auth_url)

@auth_blueprint.route('/callback')
def callback():
    error = request.args.get('error')
    code = request.args.get('code')
    state = request.args.get('state')

    if state != session.pop('state', None):
        flash('State mismatch. Please try again.', 'error')
        return redirect(url_for('auth.login'))

    if error:
        flash(f'Authorization failed: {error}', 'error')
        return redirect(url_for('auth.login'))

    token_info = exchange_code_for_token(code)
    if token_info:
        session['token_info'] = token_info
        return redirect(url_for('auth.dashboard'))
    else:
        flash('Failed to retrieve access token. Please try again.', 'error')
        return redirect(url_for('auth.login'))

@auth_blueprint.route('/dashboard')
def dashboard():
    access_token = get_access_token()
    if access_token:
        # Use the access_token to fetch Spotify data
        saved_tracks = get_saved_tracks(access_token)
        # Replace this with how you want to handle the fetched data
        return f'Accessing Spotify data... Found {len(saved_tracks)} saved tracks.'
    else:
        flash('Access token is unavailable. Please log in again.', 'warning')
        return redirect(url_for('auth.login'))



def get_access_token():
    token_info = session.get('token_info', {})
    if not token_info or is_token_expired(token_info):
        return refresh_access_token(token_info.get('refresh_token'))
    return token_info['access_token']


def is_token_expired(token_info):
    return int(time.time()) > token_info.get('expires_at', 0)

@auth_blueprint.route('/logout')
def logout():
    session.pop('token_info', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

