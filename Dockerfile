FROM python:3-slim

MAINTAINER MikiZdanovich

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "manage.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True

WORKDIR /Api

COPY requirements.txt .
RUN pip install -r requirements.txt

ADD . /Api/

EXPOSE 8000

CMD flask run --host=0.0.0.0 --port=8000