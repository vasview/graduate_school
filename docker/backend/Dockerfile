FROM python:3.10-slim

RUN addgroup -S $APP_USER && adduser -S $APP_USER -G $APP_USER

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

RUN apt-get update && apt-get install make

WORKDIR /app

COPY ./src/requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r /app/requirements.txt

COPY ./docker/backend/entrypoint.sh /app/docker/backend/

COPY ./src /app

EXPOSE 8000
