#!/bin/powershell

docker run --rm `
  -v "C:\Users\username\Desktop\app-api-aio\backup:/backup" `
  mongo `
  mongorestore --host host.docker.internal --port 27018 --db aio /backup

# Run .\dump_db.ps1