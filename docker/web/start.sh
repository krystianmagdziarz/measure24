#!/bin/sh
sleep 10
echo "1. Run migrations"
python /measure24/measure24/manage.py migrate
echo "2. Run server"
python /measure24/measure24/manage.py runserver 0.0.0.0:8000
#apache2ctl -D FOREGROUND