import logging
from typing import Optional

import backoff
import orjson
from aiokafka import AIOKafkaProducer, errors
from core import config

from db.message_broker import AbstractProducer

logger = logging.getLogger(__name__)


class KafkaProducer(AbstractProducer):
    @classmethod
    @backoff.on_exception(backoff.expo, errors.KafkaError,
                          max_tries=10, raise_on_giveup=False)
    async def start(cls, bootstrap_servers):
        self = KafkaProducer()
        self.producer = AIOKafkaProducer(
            client_id=config.PROJECT_NAME,
            bootstrap_servers=bootstrap_servers
        )
        await self.producer.start()
        logger.info('Connected to a message broker')
        return self

    def __init__(self):
        self.producer: Optional[AIOKafkaProducer] = None

    @backoff.on_exception(backoff.expo, errors.KafkaError,
                          max_tries=5, raise_on_giveup=False)
    async def send(self, topic: str, value: dict, key: str, action: str):
        value['action'] = action
        value = orjson.dumps(value)
        try:
            await self.producer.send(
                topic=topic, value=value, key=key.encode())
        except Exception:
            logger.info(
                'Message send to {topic} is failed'.format(topic=topic))
        else:
            logger.info(
                'Message sent to {topic} is success'.format(topic=topic))

    async def stop(self) -> None:
        await self.producer.stop()
