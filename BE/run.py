from app import create_app
import tensorflow

from utils import s3_util

if __name__ == '__main__':
    app = create_app()
    config = app.config

    app_host = config.get('APPLICATION_HOST')
    app_port = config.get('APPLICATION_PORT')
    app.run(host=app_host, port=app_port)