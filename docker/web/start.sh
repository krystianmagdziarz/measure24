#!/bin/sh
while ! nc -z DB_HOST DB_PORT; do sleep 1; done;
#sleep 8
echo "1. Run migrations"
python /measure24/measure24/manage.py migrate
echo "2. Run server"
python /measure24/measure24/manage.py runserver 0.0.0.0:8000
#apache2ctl -D FOREGROUND