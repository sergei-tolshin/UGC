import csv
from clickhouse_driver import Client
from datetime import datetime

client = Client('localhost')


def row_reader():
    with open('../event_data.csv') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=[
            'user_id',
            'movie_id',
            'viewed_frame',
            'event_time'
        ])
        for row in reader:
            yield [
                row['user_id'],
                row['movie_id'],
                int(row['viewed_frame']),
                datetime.strptime(row['event_time'], '%Y-%m-%d %H:%M:%S.%f')
            ]


client.execute("INSERT INTO default.views VALUES",
               (row for row in row_reader()))
