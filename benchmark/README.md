Перед исследованием необходимо создать таблицы в Clickhouse выполнив команды:
 - `docker exec -it clickhouse-node1 bash tmp/init_on_cluster.sh`
 - `docker exec -it clickhouse-node2 bash tmp/init_node_2.sh`
 - `docker exec -it clickhouse-node4 bash tmp/init_node_4.sh`

Для чистоты исследования при помощи `create_data_file.py` был сформирован CSV файл с `10 000 000` записей.
В каждое хранилище из созданного файла было загружено `10 000 000` записей.

Исследования показали, что **CLICKHOUSE** быстрее выполняет аналитические запросы, чем **VERTICA**.

------------
Вставка пачками по 1000 записей

`INSERT INTO views VALUES`

| Clickhouse | Vertica |
| ------------ | ------------ |
| 89.7 ms ± 31.4 ms | 57.9 ms ± 13.9 ms |

Вставка 1000 записей по одной
`INSERT INTO views (user_id, movie_id, viewed_frame, event_time) VALUES ('782951', 'tt5824071', 45, now())`

| Clickhouse | Vertica |
| ------------ | ------------ |
| 9.52 ms ± 12.7 ms | 12.9 ms ± 1.03 |

------------
`SELECT count(*) FROM views`

| Clickhouse | Vertica |
| ------------ | ------------ |
| 12.1 ms ± 4.65 ms | 33.7 ms ± 1.5 ms |

------------
`SELECT count(DISTINCT user_id) FROM views`

| Clickhouse | Vertica |
| ------------ | ------------ |
| 938 ms ± 139 ms | 3.2 s ± 91.5 ms |

------------
`SELECT count(DISTINCT movie_id) FROM views`

| Clickhouse | Vertica |
| ------------ | ------------ |
| 1.2 s ± 645 ms | 3.16 s ± 104 ms |

------------
`SELECT min(viewed_frame), max(viewed_frame) FROM views`

| Clickhouse | Vertica |
| ------------ | ------------ |
| 70.6 ms ± 6.89 ms | 141 ms ± 31.3 ms |

------------
`SELECT SELECT count(*), sum(viewed_frame), avg(viewed_frame) FROM views`

| Clickhouse | Vertica | |
| ------------ | ------------ | ------------ |
| 58.5 ms ± 7.4 ms | 115 ms ± 3.15 ms | |
| 124 ms ± 11.1 ms | 209 ms ± 21.6 ms | под нагрузкой |

------------
`SELECT user_id, count(distinct movie_id) FROM views GROUP by user_id`

| Clickhouse | Vertica |
| ------------ | ------------ |
| 6.53 s ± 1.34 s | 32.1 s ± 3.32 s |

------------
`SELECT movie_id, count(distinct user_id) FROM views GROUP by movie_id`

| Clickhouse | Vertica |
| ------------ | ------------ |
| 8.27 s ± 3.27 s |  25.5 s ± 3.59 s |

------------
`SELECT user_id, sum(viewed_frame), min(viewed_frame), max(viewed_frame), avg(viewed_frame) FROM views GROUP by user_id`

| Clickhouse | Vertica |
| ------------ | ------------ |
| 4.01 s ± 493 ms | 25.9 s ± 4.51 s |

------------
`SELECT movie_id, sum(viewed_frame), min(viewed_frame), max(viewed_frame), avg(viewed_frame) FROM views GROUP by movie_id`

| Clickhouse | Vertica |
| ------------ | ------------ |
| 2.92 s ± 73 ms | 17.1 s ± 4.91 s |

