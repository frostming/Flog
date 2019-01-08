# --------------------------
# Docker file
# --------------------------
FROM python:3.7

# -- Install dependencies
RUN pip install --upgrade pip

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# Application
RUN mkdir /app
WORKDIR /app
COPY requirements.txt requirements.txt

RUN set -ex && pip install -r requirements.txt
