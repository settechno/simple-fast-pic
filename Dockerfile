FROM python:3.10.10-slim AS development_build

ARG MODE

RUN apt update && apt-get -y install supervisor

ENV MODE=${MODE} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.4.0

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml /code/

# Project initialization:
WORKDIR /code
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$MODE" != "testing" && echo "--no-dev") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY ./ /code
COPY ./deploy/.env /code/.env

EXPOSE 8080

RUN mkdir data

COPY ./deploy/supervisord.conf /etc/
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
