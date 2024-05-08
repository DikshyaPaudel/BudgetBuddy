FROM python:3.10-slim-bullseye
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DB_HOST db

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .


RUN pip install -r requirements.txt
