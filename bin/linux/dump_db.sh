#!/usr/bin/bash
# -v "/home/dcbao/Desktop/app-api-aio/backup:/backup" \

docker run --rm \
  -v "$(pwd)/backup:/backup" \
  mongo \
  mongorestore --host host.docker.internal --port 27018 --db aio /backup