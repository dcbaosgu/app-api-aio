<p align="center">
  <img width="96" align="center" src="src/main/resources/static/img/logo.png" alt="logo">
</p>
  <h1 align="center">
  APP - API - AIO
</h1>
<p align="center">
  Modular website using FastAPI and MongoDB combined with many premium services including all functions from every app integrated into a closed ecosystem.
</p>

<p align="center">
    <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/FastAPI-0.100.0-blue?color=00B16A" alt="FastAPI"/>
    </a>

    <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Docker-Latest-blue?color=00B16A" alt="Docker"/>
    </a>

    <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/MongoDB-Latest-blue?color=00B16A" alt="MongoDB"/>
    </a>

    <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/RabbitMQ-Latest-blue?color=00B16A" alt="RabbitMQ"/>
    </a>

    <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Kafka-Latest-blue?color=00B16A" alt="Kafka"/>
    </a>

    <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Redis-Latest-blue?color=00B16A" alt="Redis"/>
    </a>

    <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Sentry-Latest-blue?color=00B16A" alt="Sentry"/>
    </a>
</p>

### ⚠️Notice: Everything is packaged and versioned in Docker.
## 🛠️ Notes Installation & Fix bug

# EXPORT & DELETE ALL LIBRARY
pip freeze > requirements.txt
pip freeze | ForEach-Object { pip uninstall -y $_ }

# DELETE CACHE DOCKER
docker system prune -a --volumes --force
docker builder prune --all --force

# DOCKER BUILT AND START
docker-compose build
docker-compose up --no-log-prefix

# ACCESS FOLDER DOCKER
docker exec -it app-api-aio-api-1 /bin/sh
cd /opt/python-projects/app/

# RABBITMQ NOT WORKING -> STOP -> START AGAIN
rabbitmq-plugins enable rabbitmq_management
net stop RabbitMQ && net start RabbitMQ

# URL REDIS INSIGHT CONNECT
redis://:APP-API-AIO@127.0.0.1:6379/0

# RUN POWERSHELL BACKUP
.\dump_db.ps1

# CREATE CHANNEL AND GET ID
# -> /start bot, add bot in channel (set admin) -> send channel -> get id
https://api.telegram.org/bot<BOT_TOKEN>/getUpdates

# SSH SERVER AWS
icacls .\ec2.pem /inheritance:r
icacls .\ec2.pem /grant:r "$($env:USERNAME):(R)"
icacls .\ec2.pem
ssh -i .\ec2.pem ubuntu@<PUBLIC_IP>

# INSTALL & RUN PROJECT 
cd ./project (after git clone)
sudo apt update
sudo apt install docker-compose
sudo docker-compose up
