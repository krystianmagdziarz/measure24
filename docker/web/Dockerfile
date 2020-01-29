FROM python:3.6

RUN apt-get update && apt-get install -y \
    software-properties-common \
    ca-certificates \
    curl
#    libapache2-mod-wsgi-py3 \
#    apache2 \
#    apache2-utils

ENV PYTHONUNBUFFERED 1

RUN mkdir /measure24
WORKDIR /measure24

COPY requirements.txt /measure24/
RUN pip3 install -r requirements.txt

COPY . /measure24/

ADD ./start.sh /home/start.sh
RUN chmod +x /home/start.sh

# ADD ./measure24_site.conf /etc/apache2/sites-available/000-default.conf

CMD ["sh", "/home/start.sh"]
