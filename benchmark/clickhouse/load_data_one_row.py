import csv
from datetime import datetime

from clickhouse_driver import Client

client = Client('localhost')


def insert(row):
    values = [
        row['user_id'],
        row['movie_id'],
        int(row['viewed_frame']),
        datetime.strptime(row['event_time'], '%Y-%m-%d %H:%M:%S.%f')
    ]
    client.execute("INSERT INTO default.views VALUES", [values])


if __name__ == '__main__':
    with open('../event_data.csv') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=[
            'user_id',
            'movie_id',
            'viewed_frame',
            'event_time'
        ])
        for row in reader:
            insert(row)
