#  UGC API для онлайн-кинотеатра

### Описание

Сервис для хранения пользовательского контента: лайки и оценки фильмов, рецензии к фильмам и избранные фильмы.

### Технологии
- Python 3.9
- FastAPI
- MongoDB
- Kafka
- gunicorn/uvicorn workers
- Nginx
- Docker, docker-compose

###  Запуск сервиса
1. Запустите Kafka и MongoDB в docker контейнерах:
```bash
$ docker-compose-kafka up
```
```bash
$ docker-compose-mongodb up
```
Необходимо некоторое время для запуска контейнеров.
2. Создайте необходимые топики в Kafka
3. Поднимите кластер MongoDB:
```bash
$ docker-compose exec -it mongos1 bash -c "mongo < /scripts/config_server.js"
```
```bash
$ docker-compose exec -it mongos1 bash -c "mongo < /scripts/replica_1.js"
```
```bash
$ docker-compose exec -it mongos1 bash -c "mongo < /scripts/replica_2.js"
```
```bash
$ docker-compose exec -it mongos1 bash -c "mongo < /scripts/router.js"
```
5. Создайте базу данных и коллекции в MongoDB
4. Запустите сервис UGC в docker контейнере:
```bash
$ docker-compose-ugc_api up --build
```

### Документация и доступные эндпоинты
Благодаря встроенным возможностям FastAPI, будет автоматически создана документация по api. После запуска приложения посмотреть все доступные эндпоинты и протестировать его работу можно прямо в браузере. Для этого откройте страницу <http://0.0.0.0/api/openapi> или страницу <http://0.0.0.0/api/redoc>
