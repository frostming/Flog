#!/bin/sh
set -e
PYPACKAGES=$(pdm info --packages)
export PATH=$PYPACKAGES/bin:$PATH
eval $(pdm --pep582)

FLASK_APP=flaskblog.app flask db upgrade
pybabel compile -d flaskblog/translations
PORT=${PORT:-5000}

exec gunicorn -b :${PORT} --access-logfile - --error-logfile - -k gevent -w 4 "flaskblog.app:create_app()"
