from flask import Flask
from flask_mysqldb import MySQL
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

    # MySQL configurations
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
    app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Optional: Use dictionaries for query results

    # Initialize MySQL
    mysql = MySQL(app)

    # Register blueprints
    from .auth import auth_blueprint
    from .music import music_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(music_blueprint, url_prefix='/music')

    @app.route('/')
    def index():
        return 'Welcome to SoundSurfer!'

    return app

