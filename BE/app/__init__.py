import os

from flask import Flask

from app.audio_prediction_app import mod as audio_prediction_blueprint
from app.audio_collection_app import mod as audio_collection_blueprint


def init_blueprint(app):
    # Load config
    application_root = app.config.get('APPLICATION_ROOT')
    # Register Blueprints
    app.register_blueprint(audio_collection_blueprint, url_prefix=application_root)
    app.register_blueprint(audio_prediction_blueprint, url_prefix=application_root)


# Create Flask app
def create_app():
    app = Flask(__name__)
    # Load config
    app.config.from_object('app.default_config')
    app.config.from_pyfile(os.path.join(app.instance_path, 'environment.py'))
    # Init blueprint
    init_blueprint(app)

    return app