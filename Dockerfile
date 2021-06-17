# --------------------------
# Docker file
# --------------------------
FROM python:3.9-slim

# Replace the address to a proper mirror.
ARG package_mirror=https://mirrors.tencent.com
ARG pypi_mirror=https://mirrors.tencent.com/pypi/simple

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PIP_INDEX_URL $pypi_mirror

RUN sed -i "s#http://deb.debian.org#$package_mirror#g" /etc/apt/sources.list && \
    apt-get update && apt-get install -y gcc && \
    pip install --upgrade pdm

# Application
WORKDIR /app
COPY pyproject.toml pyproject.toml
COPY pdm.lock pdm.lock
RUN pdm sync -s postgres --prod

COPY flaskblog flaskblog
COPY migrations migrations
COPY start_server.sh start_server.sh

RUN chmod a+x start_server.sh

EXPOSE 5000
ENTRYPOINT [ "./start_server.sh" ]
