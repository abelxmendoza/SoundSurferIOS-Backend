import requests
from flask import current_app, session, request, redirect, url_for
from base64 import b64encode

def get_spotify_auth_url():
    scope = "user-library-read"  # Modify this based on the required permissions
    auth_url = "https://accounts.spotify.com/authorize"
    redirect_uri = current_app.config['SPOTIFY_REDIRECT_URI']
    client_id = current_app.config['SPOTIFY_CLIENT_ID']

    auth_query = f"{auth_url}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
    return auth_query

def exchange_code_for_token(code):
    token_url = 'https://accounts.spotify.com/api/token'
    redirect_uri = current_app.config['SPOTIFY_REDIRECT_URI']
    client_id = current_app.config['SPOTIFY_CLIENT_ID']
    client_secret = current_app.config['SPOTIFY_CLIENT_SECRET']

    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = b64encode(client_creds.encode()).decode()

    headers = {
        'Authorization': f'Basic {client_creds_b64}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri
    }

    response = requests.post(token_url, headers=headers, data=data)
    token_info = response.json()
    return token_info

def get_saved_tracks(access_token):
    url = "https://api.spotify.com/v1/me/tracks"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()  # Remember to handle pagination and errors

# Additional functions to interact with Spotify API can be added here
