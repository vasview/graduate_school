FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

RUN apt-get update && apt-get install make

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r /app/requirements.txt

COPY . .

EXPOSE 8000
