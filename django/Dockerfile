FROM python:3.10

ENV PYTHONUNBUFFERD 1

RUN apt-get -y update &&\
    apt-get -y upgrade

WORKDIR /api_django

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip &&\
    pip install -r requirements.txt

COPY . .
