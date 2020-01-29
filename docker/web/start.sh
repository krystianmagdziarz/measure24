#!/bin/sh
python /measure24/measure24/manage.py migrate
python /measure24/measure24/manage.py runserver 0.0.0.0:8000
#apache2ctl -D FOREGROUND