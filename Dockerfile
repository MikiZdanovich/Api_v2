FROM python:3-slim

MAINTAINER MikiZdanovich

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "manage.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True

WORKDIR /Api

RUN pip install --upgrade pip
COPY ./requirements.txt /Api/requirements.txt
RUN pip install -r requirements.txt

ADD . /Api/


