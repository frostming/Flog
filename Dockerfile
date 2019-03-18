# --------------------------
# Docker file
# --------------------------
FROM python:3.7

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYPI_MIRROR https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install --upgrade pipenv

# Application
RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pipenv install --deploy --system
RUN chmod a+x start_server.sh
ENTRYPOINT [ "start_server.sh" ]
