#!/usr/bin/env bash

# service nginx start
# systemctl start nginx
# uwsgi --ini configs/uwsgi.ini
set -o allexport; source v1/.env_test; set +o allexport
FLASK_APP=manage.py FLASK_DEBUG=1 flask run --host=0.0.0.0 --port=5001
