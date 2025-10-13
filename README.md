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

### ⚠️Notice: Build and run the web server in Docker then load the backup dataset using scripts on any operating system

## 🛠️ Installation Steps

### 🌐 Project NextJS
1. Git clone the Project: 
   ```shell
    git clone https://github.com/Canon-D2/app-gui-aio
    ```
2. If Bun and NodeJS is not in your system
   - [Install NodeJS V22.20.0](https://nodejs.org/en/download)
   - [Install Bun V1.2.32](https://bun.com/docs/installation)

3. If you get an error when building, delete the old bun.lock and node modules.
4. Build dependencies
  ```shell
    bun install
  ```
5. Run the application
  ```shell
    bun run dev
  ```
6. Access host
  ```shell
    http://localhost:3000/
  ```

### 📱 Project RestfulAPI
1. If Docker and other ingredients is not in your system
   - [Install Docker Engine](https://docs.docker.com/engine/install/ubuntu/)
   - [Install Redis Insign](https://redis.io/docs/latest/operate/redisinsight/install/)
   - [Install Mongo Compass](https://www.mongodb.com/try/download/compass)

2. Git clone the Project:
  ```shell
    git clone https://github.com/Canon-D2/app-api-aio
  ```

3. Building Applications on Docker
  - Add env file containing environment variables to project

  - Building and Running services
  ```shell
    docker-compose build
    docker-compose up
  ```

4. Dump database
  - Put files containing data in backup folder
   ```shell
    .\bin\windows\dump_db.ps1
    ./bin/linux/dump_db.sh
  ```

5. Convert HTTP Live Streaming
  -Ensure video exists in mp4 and mov format
   ```shell
    python3 apple_hls.py
    swift apple_hls.swift
    ./bin/linux/apple_hls.sh
  ```
  
6. Run APP
  ```shell
    http://localhost:8000/docs/
    http://localhost:8000/redoc/
  ```
   
--------------------------------------------------------
<p align="center"> Thanks for reading me ❤️ </p>