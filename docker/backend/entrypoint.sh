#!/bin/sh

set -e

python manage.py migrate

python manage.py collectstatic --noinput

gunicorn config.wsgi --bind 0.0.0.0:8000 --workers 2 --threads 2
