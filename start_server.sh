#!/bin/sh

flask db upgrade
make compile
PORT=${PORT:-5000}
exec gunicorn -b :${PORT} --access-logfile - --error-logfile - -w 4 "wsgi:create_app()"
