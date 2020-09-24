#!/bin/sh
sleep 10
echo "1. Make migrations"
python /measure24/measure24/manage.py makemigrations
echo "2. Run migrations"
python /measure24/measure24/manage.py migrate
echo "3. Run server"
python /measure24/measure24/manage.py runserver 0.0.0.0:8000
#apache2ctl -D FOREGROUND