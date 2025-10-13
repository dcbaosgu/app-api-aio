#!/bin/bash
# -v "/Users/dcbao/Desktop/app-api-aio/backup:/backup" \

docker run --rm \
  --pull=never \
  -v "$(pwd)/backup:/backup" \
  mongo:8.0.15 \
  mongorestore --host host.docker.internal --port 27018 --db aio /backup