#!/bin/sh
set -e

FLASK_APP=flaskblog.app pdm run flask db upgrade
pdm run pybabel compile -d flaskblog/translations
PORT=${PORT:-5000}

exec pdm run gunicorn -b :${PORT} --access-logfile - --error-logfile - -k gevent -w 4 "flaskblog.app:create_app()"
