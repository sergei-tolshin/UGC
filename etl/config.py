from pydantic import BaseSettings


class KafkaSettings(BaseSettings):

    topic: str
    host: str
    port: int
    group_id: str
    auto_offset_reset: str
    consumer_timeout_ms: int

    class Config:
        env_prefix = 'kafka_'
        env_file = '.env'


class ClickHouseSettings(BaseSettings):

    host: str

    class Config:
        env_prefix = 'clickhouse_'
        env_file = '.env'


class ETLSettings(BaseSettings):
    key_delimeter: str
    sleep: int

    class Config:
        env_prefix = 'etl_'
        env_file = '.env'


kafka_settings = KafkaSettings()
clickhouse_settings = ClickHouseSettings()
etl_settings = ETLSettings()
