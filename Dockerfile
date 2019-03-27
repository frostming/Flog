# --------------------------
# Docker file
# --------------------------
FROM python:3.7-alpine

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apk add build-base postgresql-dev
RUN pip install --upgrade pipenv

# Application
WORKDIR /app
COPY . /app

RUN pipenv install --deploy --system
RUN chmod a+x /app/start_server.sh
ENTRYPOINT [ "/app/start_server.sh" ]
