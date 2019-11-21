# --------------------------
# Docker file
# --------------------------
FROM python:3.7-alpine

# Replace the address to a proper mirror.
ARG alpine_mirror=https://mirrors.tencent.com
ARG pypi_mirror=https://mirrors.tencent.com/pypi/simple

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PIPENV_PYPI_MIRROR $pypi_mirror
ENV PIP_INDEX_URL $pypi_mirror

RUN sed -i "s#http://dl-cdn.alpinelinux.org#$alpine_mirror#g" /etc/apk/repositories
RUN apk add build-base postgresql-dev openssl-dev libffi-dev
RUN pip install --upgrade pipfile-requirements

# Application
WORKDIR /app
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipfile2req Pipfile.lock > requirements.txt
RUN pip install -r requirements.txt

COPY flaskblog flaskblog
COPY migrations migrations
COPY start_server.sh start_server.sh

RUN chmod a+x start_server.sh

EXPOSE 5000
ENTRYPOINT [ "./start_server.sh" ]
