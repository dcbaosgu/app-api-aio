#!/usr/bin/powershell
# -v "C:\Users\dcbao\Desktop\app-api-aio\backup:/backup" `

$backupPath = Join-Path $PSScriptRoot "backup"

docker run --rm `
  --pull=never `
  -v "${backupPath}:/backup" `
  mongo:8.0.15 `
  mongorestore --host host.docker.internal --port 27018 --db aio /backup
