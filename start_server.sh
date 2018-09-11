#!/bin/sh

flask db upgrade
make compile

exec gunicorn -b :5000 --access-logfile - --error-logfile - -w 4 "wsgi:create_app()"
