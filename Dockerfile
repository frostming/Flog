# --------------------------
# Docker file
# --------------------------
FROM python:3.7

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYPI_MIRROR https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install pipfile-requirements

# Application
RUN mkdir /app
WORKDIR /app
# -- Install dependencies
COPY Pipfile.lock Pipfile.lock
RUN pipfile2req > requirements.txt
RUN pip install -i ${PYPI_MIRROR} -r requirements.txt
