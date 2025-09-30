#!/usr/bin/powershell
# -v "C:\Users\dcbao\Desktop\app-api-aio\backup:/backup" `

$backupPath = Join-Path $PSScriptRoot "backup"

docker run --rm `
  -v "$backupPath:/backup" `
  mongo `
  mongorestore --host host.docker.internal --port 27018 --db aio /backup
