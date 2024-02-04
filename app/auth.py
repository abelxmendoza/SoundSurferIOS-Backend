from flask import Blueprint, session, request, redirect, url_for, flash
import requests
from base64 import b64encode
import os
import time
import uuid


# Adjusted environment variable names for clarity
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
SCOPE = os.getenv('SPOTIFY_SCOPE', 'user-library-read')

auth_blueprint = Blueprint('auth', __name__)

@app.route('/login')
def login():
    state = str(uuid.uuid4())
    session['state'] = state

    auth_url = ("https://accounts.spotify.com/authorize?" +
                f"response_type=code&client_id={CLIENT_ID}&scope={SCOPE}" +
                f"&redirect_uri={REDIRECT_URI}&state={state}")
    return redirect(auth_url)

@app.route('/callback')
def callback():
    error = request.args.get('error')
    code = request.args.get('code')
    state = request.args.get('state')

    if state != session.pop('state', None):
        flash('State mismatch. Please try again.', 'error')
        return redirect(url_for('.login'))

    if error:
        flash(f'Authorization failed: {error}', 'error')
        return redirect(url_for('.login'))

    token_info = exchange_code_for_token(code)
    if token_info:
        session['token_info'] = token_info
        return redirect(url_for('.dashboard'))
    else:
        flash('Failed to retrieve access token. Please try again.', 'error')
        return redirect(url_for('.login'))

def exchange_code_for_token(code):
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {
        'Authorization': f'Basic {b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post('https://accounts.spotify.com/api/token', data=payload, headers=headers)
    if response.ok:
        return response.json()
    else:
        print(f"Failed to exchange code for token: {response.text}")
        return None

@app.route('/refresh_token')
def refresh_access_token():
    token_info = session.get('token_info', {})
    refresh_token = token_info.get('refresh_token')
    if not refresh_token:
        flash('No refresh token available.', 'error')
        return redirect(url_for('.login'))

    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    headers = {
        'Authorization': f'Basic {b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post('https://accounts.spotify.com/api/token', data=payload, headers=headers)
    if response.ok:
        new_token_info = response.json()
        token_info.update(new_token_info)
        token_info['expires_at'] = int(time.time()) + new_token_info['expires_in']
        session['token_info'] = token_info
        return redirect(url_for('.dashboard'))
    else:
        print(f"Failed to refresh access token: {response.text}")
        flash('Failed to refresh access token.', 'error')
        return redirect(url_for('.login'))

@app.route('/logout')
def logout():
    session.pop('token_info', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('.login'))

@app.route('/dashboard')
def dashboard():
    access_token = get_access_token()
    if access_token:
        # Placeholder for actual Spotify data fetching
        return 'Accessing Spotify data...'
    else:
        flash('Access token is unavailable. Please log in again.', 'warning')
        return redirect(url_for('.login'))

def is_token_expired(token_info):
    return int(time.time()) > token_info.get('expires_at', 0)

def get_access_token():
    token_info = session.get('token_info', {})
    if not token_info or is_token_expired(token_info):
        return refresh_access_token()
    return token_info['access_token']

