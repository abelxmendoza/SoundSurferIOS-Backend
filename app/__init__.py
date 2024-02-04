from flask import Flask
from .auth import auth_blueprint
# If you have other blueprints, import them here
# from .views import main_blueprint

def create_app():
    app = Flask(__name__)

    # Basic configuration
    app.config['SECRET_KEY'] = 'your_secret_key'  # Use a secure secret key
    # You can also load more configurations from a separate file
    # app.config.from_pyfile('config.py')

    # Register blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    # Register other blueprints as needed
    # app.register_blueprint(main_blueprint)

    return app
