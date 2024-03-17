# music.py
import requests
from flask import Blueprint, request, jsonify, current_app
from .spotify import get_spotify_access_token

music_blueprint = Blueprint('music', __name__)

@music_blueprint.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    filters = data.get('filters', {})

    if not filters or len(filters) > 2:
        return jsonify({"error": "Please provide at least 1 and at most 2 filters"}), 400

    # Get access token for Spotify API
    access_token = get_spotify_access_token()
    if not access_token:
        return jsonify({"error": "Failed to authenticate with Spotify"}), 401

    recommendations = fetch_spotify_recommendations(filters, access_token)

    return jsonify(recommendations)

def fetch_spotify_recommendations(filters, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    # Construct the query parameters based on filters provided
    params = {f"target_{key}": value for key, value in filters.items()}

    response = requests.get("https://api.spotify.com/v1/recommendations", headers=headers, params=params)

    if response.status_code == 200:
        # Parse and return the recommendations from the response
        return response.json()['tracks']
    else:
        # Handle errors from the Spotify API
        print(f"Error fetching recommendations: {response.json()}")
        return []
