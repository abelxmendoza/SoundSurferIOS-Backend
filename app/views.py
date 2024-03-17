from flask import Blueprint, request, jsonify
from .db_operations import create_user, get_user_by_spotify_id, like_song, unlike_song, get_liked_songs, update_user, delete_user
from .ml_model_integration import get_temporary_playlist  # Import the ML model integration

# Blueprint for main application routes
main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    return "Welcome to SoundSurfer!"

# Temporary Playlist Generation Route
@main_blueprint.route('/generate_playlist', methods=['POST'])
def generate_playlist():
    data = request.json
    song_name = data.get('song_name')
    filters = data.get('filters', {})
    playlist = get_temporary_playlist(song_name, filters)
    return jsonify({'playlist': playlist}), 200

# User Routes
@main_blueprint.route('/user', methods=['POST'])
def add_user():
    # Existing code...

@main_blueprint.route('/user/<spotify_user_id>', methods=['GET'])
def user_details(spotify_user_id):
    # Existing code...

@main_blueprint.route('/user/<spotify_user_id>', methods=['PUT'])
def update_user_details(spotify_user_id):
    # Existing code...

@main_blueprint.route('/user/<spotify_user_id>', methods=['DELETE'])
def remove_user(spotify_user_id):
    # Existing code...

# Song Routes
@main_blueprint.route('/user/<spotify_user_id>/likes', methods=['GET'])
def user_liked_songs(spotify_user_id):
    # Existing code...

@main_blueprint.route('/user/<spotify_user_id>/like', methods=['POST'])
def add_like(spotify_user_id):
    # Existing code...

@main_blueprint.route('/user/<spotify_user_id>/unlike', methods=['POST'])
def remove_like(spotify_user_id):
    # Existing code...

# Continue adding more routes as needed...
