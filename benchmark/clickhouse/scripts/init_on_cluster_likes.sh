#!/bin/bash
set -e

clickhouse-client -h localhost -n <<-EOSQL
    CREATE DATABASE IF NOT EXISTS simple ON CLUSTER 'company_cluster';
    CREATE TABLE IF NOT EXISTS simple.movieAnaliticsDb ON CLUSTER 'company_cluster' (
        date Date,
        user_id String,
        movie_id String,
        score UInt8,
        mark UInt8,
        text Text
    ) Engine=MergeTree(date, (user_id, movie_id), 1)
EOSQL