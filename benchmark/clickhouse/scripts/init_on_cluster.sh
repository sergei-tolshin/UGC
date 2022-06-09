#!/bin/bash
set -e

clickhouse-client -h localhost -n <<-EOSQL
    CREATE DATABASE IF NOT EXISTS shard ON CLUSTER 'company_cluster';
    CREATE TABLE IF NOT EXISTS shard.views ON CLUSTER 'company_cluster' (
        user_id String,
        movie_id String,
        viewed_frame UInt64,
        event_time DateTime
    ) Engine=ReplicatedMergeTree('/clickhouse/tables/shard{shard}/views', '{replica}')
    PARTITION BY toYYYYMMDD(event_time)
    ORDER BY user_id;
    CREATE TABLE IF NOT EXISTS default.views ON CLUSTER 'company_cluster' AS shard.views
    ENGINE = Distributed('company_cluster', shard, views, rand());
EOSQL