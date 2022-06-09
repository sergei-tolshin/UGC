import csv
import vertica_python
from datetime import datetime

connection_info = {
    'host': '127.0.0.1',
    'port': 5433,
    'user': 'dbadmin',
    'password': '',
    'database': 'docker',
    'autocommit': True,
}


def create_table():
    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS views (
            id IDENTITY,
            user_id VARCHAR(256) NOT NULL,
            movie_id VARCHAR(256) NOT NULL,
            viewed_frame INTEGER NOT NULL,
            event_time DATETIME
        );
        """)


def insert(values):
    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()
        query = "INSERT INTO views (user_id, movie_id, viewed_frame, event_time) VALUES (%s,%s,%s,%s)"
        cursor.executemany(query, values)


if __name__ == '__main__':
    create_table()
    with open('../event_data.csv') as csvfile:
        values = []
        reader = csv.DictReader(csvfile, fieldnames=[
            'user_id',
            'movie_id',
            'viewed_frame',
            'event_time'
        ])
        for row in reader:
            values.append([
                row['user_id'],
                row['movie_id'],
                int(row['viewed_frame']),
                datetime.strptime(row['event_time'], '%Y-%m-%d %H:%M:%S.%f')
            ])
            if len(values) == 1000:
                insert(values)
                values = []
        if values:
            insert(values)
