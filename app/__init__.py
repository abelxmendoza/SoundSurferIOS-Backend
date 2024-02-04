from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Set the secret key for session management
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

    # Set Spotify configuration variables
    app.config['SPOTIFY_CLIENT_ID'] = os.getenv('SPOTIFY_CLIENT_ID')
    app.config['SPOTIFY_CLIENT_SECRET'] = os.getenv('SPOTIFY_CLIENT_SECRET')
    app.config['SPOTIFY_REDIRECT_URI'] = os.getenv('SPOTIFY_REDIRECT_URI')
    app.config['SPOTIFY_SCOPE'] = os.getenv('SPOTIFY_SCOPE', 'user-library-read')

    # Register blueprints
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    @app.route('/')
    def index():
        return 'Welcome to SoundSurfer!'

    return app
