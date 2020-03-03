FROM python:3-slim

MAINTAINER MikiZdanovich

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "manage.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True

WORKDIR /api

RUN pip install --upgrade pip
COPY ./requirements.txt ./requirements/
RUN pip install -r ./requirements/requirements.txt
COPY alembic.ini ./
COPY alembic ./alembic
COPY test ./test
ADD ./backend ./backend
CMD "gunicorn -b 0.0.0.0:5000  --max-requests 1000 --timeout 60 backend.wsgi:app"

