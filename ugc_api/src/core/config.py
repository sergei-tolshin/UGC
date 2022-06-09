import os
from logging import config as logging_config
from pathlib import Path

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies_ugc')

# Настройки Kafka
KAFKA_HOST = os.getenv('KAFKA_HOST', '127.0.0.1')
KAFKA_PORT = int(os.getenv('KAFKA_PORT', 9092))

# Настройки MongoDB
MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://localhost:27017/?authSource=ugc_db')
MONGODB_DB = os.getenv('MONGODB_DB', 'ugc_db')
if not MONGODB_URL:
    MONGODB_HOST = os.getenv('MONGODB_HOST', 'localhost')
    MONGODB_PORT = int(os.getenv('MONGODB_PORT', 27017))
    MONGODB_USER = os.getenv('MONGODB_USER', 'admin')
    MONGODB_PASS = os.getenv('MONGODB_PASS', '')

    MONGODB_URL = f'mongodb://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DB}'

# Корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Локализация
LANGUAGE = os.getenv('LANGUAGE', 'ru')
LOCALE_PATH = os.getenv('LOCALE_PATH', 'locale')

# Сервис авторизации
AUTH_GRPC_HOST = os.getenv('AUTH_GRPC_HOST', '127.0.0.1')
AUTH_GRPC_PORT = os.getenv('AUTH_GRPC_PORT', '50051')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'secret_key')
JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', 'HS256')

# Sentry
SENTRY_DSN = os.getenv('SENTRY_DSN', 'https://cd876fdfc3744d36b1507404a4e6cb55@o1281274.ingest.sentry.io/6487131')
