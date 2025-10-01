<p align="center">
  <img width="96" src="https://ttnnth-tinhoc.sgu.edu.vn/wp-content/uploads/2018/11/SGU-LOGO-600x600.png" alt="logo">
</p>

<h1 align="center">APP - API - AIO</h1>

<p align="center">
  Modular website using FastAPI and MongoDB combined with many premium services including all functions from every app integrated into a closed ecosystem.
</p>

<p align="center">
  <a href="https://fastapi.tiangolo.com/">
    <img src="https://img.shields.io/badge/FastAPI-0.100.0-blue?color=00B16A" alt="FastAPI">
  </a>
  <a href="https://www.docker.com/">
    <img src="https://img.shields.io/badge/Docker-Latest-blue?color=00B16A" alt="Docker">
  </a>
  <a href="https://www.mongodb.com/">
    <img src="https://img.shields.io/badge/MongoDB-Latest-blue?color=00B16A" alt="MongoDB">
  </a>
  <a href="https://www.rabbitmq.com/">
    <img src="https://img.shields.io/badge/RabbitMQ-Latest-blue?color=00B16A" alt="RabbitMQ">
  </a>
  <a href="https://kafka.apache.org/">
    <img src="https://img.shields.io/badge/Kafka-Latest-blue?color=00B16A" alt="Kafka">
  </a>
  <a href="https://redis.io/">
    <img src="https://img.shields.io/badge/Redis-Latest-blue?color=00B16A" alt="Redis">
  </a>
  <a href="https://sentry.io/">
    <img src="https://img.shields.io/badge/Sentry-Latest-blue?color=00B16A" alt="Sentry">
  </a>
</p>

### ⚠️Notice: Everything is packaged and versioned in Docker.
## 🛠️ Notes Installation & Fix bug

# EXPORT REQUIMENT & DELETE ALL LIBRARY
pip freeze > requirements.txt
pip freeze | ForEach-Object { pip uninstall -y $_ }

# DELETE CACHE DOCKER
docker stop $(docker ps -q) 2>/dev/null
docker system prune -a --volumes --force && docker builder prune -a --force

# DOCKER BUILT AND START
cd ./project_name
docker-compose build
docker-compose up --no-log-prefix

# ACCESS FOLDER DOCKER
docker exec -it app-api-aio-api-1 /bin/sh
cd /opt/python-projects/apps/

# CHECK VERSION SERVICES
docker exec -it app-api-aio-mgdb-1 mongod --version
docker exec -it nginx nginx -v
docker exec -it app-api-aio-rabbitmq-1 rabbitmqctl version

# RABBITMQ NOT WORKING -> STOP -> START AGAIN
rabbitmq-plugins enable rabbitmq_management
net stop RabbitMQ && net start RabbitMQ

# URL REDIS INSIGHT CONNECT
redis://:APP-API-AIO@127.0.0.1:6379/0

# RUN DATA BACKUP
.\bin\windows\dump_db.ps1 (windows)

chmod +x /bin/linux/dump_db.sh (linux)
./bin/linux/dump_db.sh

chmod +x ./bin/macos/dump_db.command (macos)      
./bin/linux/dump_db.sh

# CREATE CHANNEL AND GET ID
# (start bot, add bot in channel (set admin) -> send channel -> get id)
https://api.telegram.org/bot<BOT_TOKEN>/getUpdates

# CALL WEBSOCET
ws://localhost:8000/chat/ws/<channel_id>

# RUN pytest in docker
docker exec -it app-api-aio-api-1 \

sh -c "PYTHONPATH=/opt/python-projects/apps pytest -p no:warnings /opt/python-projects/apps/test/test_ping.py"

# SSH SERVER AWS
icacls .\ec2.pem /inheritance:r
icacls .\ec2.pem /grant:r "$($env:USERNAME):(R)"
chmod 400 ~/Desktop/ec2.pem (if linux)
icacls .\ec2.pem
ssh -i .\ec2.pem ubuntu@<PUBLIC_IP>