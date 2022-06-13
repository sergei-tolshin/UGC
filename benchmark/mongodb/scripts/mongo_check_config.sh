docker exec -it mongocfg1 bash -c 'echo "rs.status()" | mongosh --quiet'
docker exec -it mongors1n1 bash -c 'echo "rs.status()" | mongosh --quiet'
docker exec -it mongos1 bash -c 'echo "sh.status()" | mongosh --quiet'
