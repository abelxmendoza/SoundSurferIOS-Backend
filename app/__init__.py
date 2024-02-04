from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Configuration loading
    app.config.from_pyfile('config.py')

    # Register Blueprints
    from .views import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
