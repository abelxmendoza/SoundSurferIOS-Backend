from flask import Flask, render_template
from .auth import auth_blueprint
# Import other blueprints if you have any

def create_app():
    app = Flask(__name__)
    # app configuration settings...

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    # Register other blueprints...

    @app.route('/')
    def index():
        return 'Welcome to SoundSurfer!'

    return app
