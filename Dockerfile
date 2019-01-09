# --------------------------
# Docker file
# --------------------------
FROM python:3.7

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PIPENV_PYPI_MIRROR https://pypi.tuna.tsinghua.edu.cn/simple

# -- Install dependencies
RUN pip install --upgrade pip && pip install -U -i ${PIPENV_PYPI_MIRROR} pipenv

# Application
RUN mkdir /app
WORKDIR /app
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --pypi-mirror=${PIPENV_PYPI_MIRROR} --deploy --system
