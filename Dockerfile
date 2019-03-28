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
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
COPY flaskblog flaskblog
COPY migrations migrations
COPY start_server.sh start_server.sh
COPY wsgi.py wsgi.py
COPY Makefile Makefile

RUN pipenv install --deploy --system
RUN chmod a+x start_server.sh

EXPOSE 5000
ENTRYPOINT [ "./start_server.sh" ]
