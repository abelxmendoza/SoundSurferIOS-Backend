import requests
from flask import current_app, jsonify
from base64 import b64encode

# Fetch music recommendations based on seed tracks and additional filters
def get_recommendations(access_token, seed_tracks, filters):
    recommendations_url = "https://api.spotify.com/v1/recommendations"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "seed_tracks": seed_tracks,
        # Add other filters like 'min_energy', 'max_valence', etc.
    }
    params.update(filters)
    response = requests.get(recommendations_url, headers=headers, params=params)
    if response.ok:
        return response.json()['tracks']  # List of recommended tracks
    else:
        # Handle errors
        return None

# Add a track to the user's saved tracks
def add_track_to_saved(access_token, track_id):
    url = f"https://api.spotify.com/v1/me/tracks?ids={track_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.put(url, headers=headers)
    return response.ok

# Remove a track from the user's saved tracks
def remove_track_from_saved(access_token, track_id):
    url = f"https://api.spotify.com/v1/me/tracks?ids={track_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.delete(url, headers=headers)
    return response.ok

# Function to exchange the authorization code for access and refresh tokens
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


