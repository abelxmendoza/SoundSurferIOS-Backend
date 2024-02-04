import requests
from flask import current_app, session, request, redirect, url_for
from base64 import b64encode
import os

def get_spotify_auth_url(scopes=None):
    base_auth_url = "https://accounts.spotify.com/authorize"
    client_id = current_app.config['SPOTIFY_CLIENT_ID']
    redirect_uri = current_app.config['SPOTIFY_REDIRECT_URI']
    if not scopes:
        scopes = "user-library-read"  # Default scope
    else:
        scopes = " ".join(scopes)  # Join multiple scopes with space

    auth_query = (f"{base_auth_url}?client_id={client_id}&response_type=code"
                  f"&redirect_uri={redirect_uri}&scope={scopes}")
    return auth_query

def exchange_code_for_token(code):
    token_url = 'https://accounts.spotify.com/api/token'
    client_id = current_app.config['SPOTIFY_CLIENT_ID']
    client_secret = current_app.config['SPOTIFY_CLIENT_SECRET']
    redirect_uri = current_app.config['SPOTIFY_REDIRECT_URI']

    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = b64encode(client_creds.encode()).decode()

    headers = {'Authorization': f'Basic {client_creds_b64}',
               'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': redirect_uri}

    response = requests.post(token_url, headers=headers, data=data)
    if response.ok:
        return response.json()  # Contains access_token, refresh_token, expires_in
    else:
        # Log error or handle it accordingly
        return None

def get_saved_tracks(access_token):
    url = "https://api.spotify.com/v1/me/tracks"
    headers = {"Authorization": f"Bearer {access_token}"}
    tracks = []

    while url:
        response = requests.get(url, headers=headers)
        if response.ok:
            data = response.json()
            tracks.extend(data['items'])
            url = data['next']  # URL for the next page
        else:
            # Log error or break the loop
            break

    return tracks

def refresh_access_token(refresh_token):
    token_url = 'https://accounts.spotify.com/api/token'
    client_id = current_app.config['SPOTIFY_CLIENT_ID']
    client_secret = current_app.config['SPOTIFY_CLIENT_SECRET']

    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = b64encode(client_creds.encode()).decode()

    headers = {'Authorization': f'Basic {client_creds_b64}',
               'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}

    response = requests.post(token_url, headers=headers, data=data)
    if response.ok:
        return response.json()  # Contains new access_token and possibly a new refresh_token
    else:
        # Log error or handle it accordingly
        return None
