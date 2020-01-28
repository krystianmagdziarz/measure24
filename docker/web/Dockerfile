FROM python:3.6

RUN apt-get update && apt-get install -y \
    software-properties-common \
    ca-certificates \
    unzip \
    curl \
    xvfb \
#    firefox \
    libapache2-mod-wsgi-py3 \
    apache2 \
    apache2-utils

ENV PYTHONUNBUFFERED 1

RUN mkdir /measure24
WORKDIR /measure24

#RUN pg_config

RUN pip install --upgrade pip
COPY requirements.txt /measure24/
RUN pip3 install -r requirements.txt
COPY . /measure24/

# CMD ["python", "/measure24/measure24/manage.py", "migrate"]
CMD ["python", "/measure24/measure24/manage.py", "runserver", "0.0.0.0:8000"]

#ADD ./measure24_site.conf /etc/apache2/sites-available/000-default.conf
#CMD ["apache2ctl", "-D", "FOREGROUND"]
