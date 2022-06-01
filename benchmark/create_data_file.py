import csv
import random
import string
from datetime import datetime, timedelta
from multiprocessing import Pool


def date_between(start, end):
    start = datetime.strptime(start, '%Y-%m-%d')
    end = datetime.strptime(end, '%Y-%m-%d')

    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    random_microseconds = random.randint(1, int_delta)
    return start + timedelta(seconds=random_second,
                             microseconds=random_microseconds)


def generate_movie_id(length=7):
    letters_and_digits = string.digits
    rand_string = ''.join(random.sample(letters_and_digits, length))
    return 'tt'+rand_string


def data_row(x=0):
    return {
        'user_id': str(random.randint(1, 1000000)),
        'movie_id': generate_movie_id(),
        # возьмем среднюю продолжительность фильма 120 мин.
        # будем сохранять каждые 30 сек. просмотра
        'viewed_frame': random.randint(1, (60*60*2)/30),
        'event_time': date_between('2022-05-23', '2022-05-30')
    }


if __name__ == '__main__':
    with open('event_data.csv', 'a', encoding='utf8', newline='') as csvfile:
        w = csv.writer(csvfile)
        with Pool(4) as pool:
            for r in pool.map(data_row, range(0, 10000000)):
                w.writerow(r.values())
