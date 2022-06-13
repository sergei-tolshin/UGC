#!/bin/bash
set -e

clickhouse-client -h localhost -n <<-EOSQL
    CREATE DATABASE IF NOT EXISTS replica;
    CREATE TABLE IF NOT EXISTS replica.movieAnaliticsDb (
        user_id String,
        movie_id String,
        score UInt8,
        mark UInt8,
        text Text
    ) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/movieAnaliticsDb', '{replica}') 
    ORDER BY user_id;
EOSQL