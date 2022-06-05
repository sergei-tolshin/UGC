import aiokafka
import sentry_sdk

from fastapi import FastAPI, APIRouter

from core.logger import log
from core import config


router = APIRouter()
app = FastAPI()

sentry_sdk.init(
    "https://f26a6d2fcc4a42adb0e795cb90e3c5a3@o1275786.ingest.sentry.io/6471092",
    traces_sample_rate=1.0
)

producer = None


@app.on_event("startup")
async def startup_event():
    log.info("Initializing API ...")
    await initialize()


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down API")
    try:
        await producer.stop()
    except Exception:
        log.exception("initialize")


async def initialize():
    global producer
    producer = aiokafka.AIOKafkaProducer(
        bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS
    )
    try:
        await producer.start()
    except Exception:
        log.exception("initialize")
        await producer.stop()


async def produce(value):
    await producer.send(config.KAFKA_TOPIK, value)
