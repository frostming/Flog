#!/bin/sh
set -e
PYPACKAGES=__pypackages__/3.7
export PATH=$PYPACKAGES/bin:$PATH
export PYTHONPATH=$PYPACKAGES/lib
FLASK_APP=flaskblog.app flask db upgrade
pybabel compile -d flaskblog/translations
PORT=${PORT:-5000}
exec gunicorn -b :${PORT} --access-logfile - --error-logfile - -k gevent -w 4 "flaskblog.app:create_app()"
