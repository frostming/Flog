# --------------------------
# Docker file
# --------------------------
FROM python:3.7

# -- Install dependencies
RUN pip install --upgrade pipenv

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# Application
RUN mkdir /app
COPY . /app
WORKDIR /app

RUN set -ex && pipenv install --deploy --system

RUN chmod a+x start_server.sh
