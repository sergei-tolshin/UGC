import logging

import grpc
import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from api.v1 import favorites, reviews, scores, views
from core import config
from core import logger as logger_config
from core.middleware import AuthMiddleware, LoggingMiddleware
from db import kafka, message_broker, mongodb, storage

sentry_sdk.init(dsn=config.SENTRY_DSN)
logger = logging.getLogger(__name__)

app = FastAPI(
    title='UGC API для онлайн-кинотеатра',
    description=('User Generated Content'),
    version='1.0.0',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    redoc_url='/api/redoc',
    default_response_class=ORJSONResponse,
)

app.add_middleware(SentryAsgiMiddleware)
app.add_middleware(LoggingMiddleware, logger=logger)
app.add_middleware(
    AuthMiddleware,
    secret_key=config.JWT_SECRET_KEY,
    algorithms=config.JWT_ALGORITHM,
    auth_channel=grpc.aio.insecure_channel(
        f'{config.AUTH_GRPC_HOST}:{config.AUTH_GRPC_PORT}')
)


@app.on_event('startup')
async def startup():
    storage.db = mongodb.MongoDBStorage(
        client=AsyncIOMotorClient(
            config.MONGODB_URL,
            uuidRepresentation='standard'
        )
    )
    message_broker.producer = await kafka.KafkaProducer.start(
        bootstrap_servers=[f'{config.KAFKA_HOST}:{config.KAFKA_PORT}'])


@app.on_event('shutdown')
async def shutdown():
    await storage.db.close()
    await message_broker.producer.stop()


app.include_router(scores.router, prefix='/api/v1/scores',
                   tags=['Оценки фильмов'])
app.include_router(favorites.router, prefix='/api/v1',
                   tags=['Избранные фильмы'])
app.include_router(reviews.router, prefix='/api/v1',
                   tags=['Рецензии к фильмам'])
app.include_router(views.router, prefix='/api/v1/views',
                   tags=['Прогресс просмотра'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=logger_config.LOGGING,
        log_level=logging.DEBUG,
    )
