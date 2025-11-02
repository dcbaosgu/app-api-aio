FROM python:3.14.0-alpine

WORKDIR /opt/python-project/app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY ./requirements.txt .

RUN set -eux; \
    apk add --no-cache --virtual .build-deps \
        build-base \
        python3-dev \
        librdkafka-dev \
        libffi-dev \
        openssl-dev; \
    pip install --no-cache-dir --upgrade pip setuptools wheel; \
    pip install --no-cache-dir -r requirements.txt; \
    apk add --no-cache ffmpeg curl openssl; \
    apk del .build-deps; \
    rm -rf /root/.cache/pip

COPY . /opt/python-project/app
