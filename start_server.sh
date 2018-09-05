#!/bin/sh

flask db upgrade

exec gunicorn -b :5000 --access-logfile - --error-logfile - -w 4 wsgi:app
