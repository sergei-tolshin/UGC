#!/bin/bash
set -e

clickhouse-client -h localhost -n <<-EOSQL
    CREATE DATABASE IF NOT EXISTS shard ON CLUSTER 'company_cluster';
    CREATE TABLE IF NOT EXISTS shard.movieAnaliticsDb ON CLUSTER 'company_cluster' (
        user_id String,
        movie_id String,
        score UInt8,
        mark UInt8,
        text Text
    ) Engine=ReplicatedMergeTree('/clickhouse/tables/shard{shard}/movieAnaliticsDb', '{replica}')
    ORDER BY user_id;
    CREATE TABLE IF NOT EXISTS default.movieAnaliticsDb ON CLUSTER 'company_cluster' AS shard.movieAnaliticsDb
    ENGINE = Distributed('company_cluster', shard, movieAnaliticsDb, rand());
EOSQL