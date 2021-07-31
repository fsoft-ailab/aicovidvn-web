import os
from dotenv import load_dotenv

APPLICATION_ROOT = os.getenv('APP_ROOT', "/apis")
APPLICATION_HOST = os.getenv('APP_HOST', "0.0.0.0")
APPLICATION_PORT = os.getenv('APP_PORT', 5000)
LOG_LEVEL = os.getenv('LOG_LEVEL', "INFO")

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
AWS_GET_EXPIRED = os.getenv('AWS_GET_EXPIRED', '')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_NAME = os.getenv('DB_NAME', 'sounddr')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_PORT = os.getenv('DB_PORT', '5432')
AUDIO_FILTER = int(os.getenv('AUDIO_FILTER', 1))
NOISE_DURATION_WEIGHT_FILTER = float(os.getenv('NOISE_FILTER', 0.3))
LENGTH_FILTER = int(os.getenv('LENGTH_FILTER', 10))

S3_BUCKET = os.getenv('S3_BUCKET', '')
S3_REGION = os.getenv('S3_REGION', '')
