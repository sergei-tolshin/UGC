docker-compose exec -it mongors1n1 bash -c "mongo < /scripts/replica_1.js"
docker-compose exec -it mongors2n1 bash -c "mongo < /scripts/replica_2.js"