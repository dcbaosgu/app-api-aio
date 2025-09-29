#!/bin/bash

docker run --rm \
  -v "/home/username/Desktop/app-api-aio/backup:/backup" \
  mongo \
  mongorestore --host host.docker.internal --port 27018 --db aio /backup

# chmod +x dump_db.sh
# Run ./dump_db.sh