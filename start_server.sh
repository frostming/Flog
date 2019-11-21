#!/bin/sh
set -e
FLASK_APP=flaskblog.app flask db upgrade
pybabel compile -d flaskblog/translations
PORT=${PORT:-5000}
exec gunicorn -b :${PORT} --access-logfile - --error-logfile - -k gevent -w 8 "flaskblog.app:create_app()"
