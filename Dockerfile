FROM python:3.11.4-slim-buster

WORKDIR /usr/src/vehicle_detection_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update \
    && apt-get install -y build-essential libgl1-mesa-dev libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
COPY /requirements/app_requirements.txt .
RUN pip install -r app_requirements.txt


# copy project
COPY vehicle_detection_app .

