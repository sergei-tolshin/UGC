import datetime as dt
import logging
from dataclasses import astuple
from time import sleep

import backoff
from clickhouse_driver import Client
from clickhouse_driver.errors import NetworkError
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from config import clickhouse_settings, kafka_settings, etl_settings
from models import ViewedFrameRecord


class KafkaService:

    def __init__(self, settings=kafka_settings):
        self.settings = settings
        self.consumer = self.get_consumer()

    @backoff.on_exception(backoff.expo, NoBrokersAvailable, max_tries=20)
    def get_consumer(self):
        logger.info('Connecting to Kafka...')
        consumer = KafkaConsumer(
            self.settings.topic,
            bootstrap_servers=[
                f'{self.settings.host}:{self.settings.port}'
            ],
            auto_offset_reset=self.settings.auto_offset_reset,
            group_id=self.settings.group_id,
            consumer_timeout_ms=self.settings.consumer_timeout_ms,
        )
        logger.info('Connection to Kafka is established')
        return consumer

    def extract_data(self):
        messages = [record for record in self.consumer]
        if messages:
            logger.info('Extracted %s records from Kafka', len(messages))
        return messages

    def commit(self):
        self.consumer.commit()

    def close(self):
        self.consumer.close()


class ClickHouseService:

    def __init__(self, settings=clickhouse_settings):
        self.settings = settings
        self.client = self.get_client()

    def get_client(self):
        logger.info('Connecting to ClickHouse...')
        client = Client(host=self.settings.host)
        logger.info('Connection to ClickHouse is established')
        return client

    def close(self):
        self.client.disconnect()

    @backoff.on_exception(backoff.expo, NetworkError, max_tries=20)
    def load_data(self, events):
        count = self.client.execute("INSERT INTO default.views VALUES",
                                    (astuple(event) for event in events))
        logger.info('Loaded %s records in ClickHouse', count)


class ETL:

    def __init__(self, settings=etl_settings):
        self.settings = settings
        self.kafka_client = None
        self.clickhouse_client = None

    def __enter__(self):
        logger.info('Running ETL process...')
        self.kafka_client = KafkaService()
        self.clickhouse_client = ClickHouseService()
        return self

    def __exit__(self, type, value, traceback):
        logger.info('Closing connections...')
        if self.kafka_client is not None:
            self.kafka_client.close()
        if self.clickhouse_client is not None:
            self.clickhouse_client.close()
        logger.info('Connections are closed.')

    def sleep(self):
        logger.info('ETL process stopped for %d s.', self.settings.sleep)
        sleep(self.settings.sleep)

    def extract(self):
        return self.kafka_client.extract_data()

    def transform(self, messages):
        for message in messages:
            user_id, movie_id = message.key.decode().split(
                self.settings.key_delimeter)
            viewed_frame = int(message.value.decode())
            event_time = dt.datetime.fromtimestamp(message.timestamp/1000)
            yield ViewedFrameRecord(
                user_id, movie_id, viewed_frame, event_time
            )

    def commit(self):
        self.kafka_client.commit()

    def load(self, transform_data):
        self.clickhouse_client.load_data(transform_data)


def setup_external_logger():
    logging.getLogger('kafka').setLevel(logging.CRITICAL)
    logging.getLogger('backoff').addHandler(logging.StreamHandler())


def setup_logger():
    _log_format = ('%(asctime)s - [%(levelname)s] - %(name)s '
                   '(%(filename)s).%(funcName)s(%(lineno)d) > %(message)s')
    logging.basicConfig(
        level=logging.INFO,
        format=_log_format,
        datefmt='%Y-%m-%d %H:%M:%S')
    _logger = logging.getLogger(__name__)
    return _logger


def start_etl():

    with ETL() as etl:
        while True:
            messages = etl.extract()
            if messages:
                transform_data = etl.transform(messages)
                etl.load(transform_data)
            etl.commit()
            etl.sleep()


if __name__ == '__main__':
    setup_external_logger()
    logger = setup_logger()
    try:
        start_etl()
    except KeyboardInterrupt:
        logger.info('ETL process manually interrupted')
