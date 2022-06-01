CREATE DATABASE IF NOT EXISTS replica;

CREATE TABLE IF NOT EXISTS replica.views (
    user_id String,
    movie_id String,
    viewed_frame UInt64,
    event_time DateTime
) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/views', '{replica}') 
PARTITION BY toYYYYMMDD(event_time)
ORDER BY user_id;