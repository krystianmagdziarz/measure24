FROM python:3.6

RUN apt-get update && apt-get install -y \
    software-properties-common \
    ca-certificates \
    curl

ENV PYTHONUNBUFFERED 1

RUN mkdir /measure24
WORKDIR /measure24

COPY requirements.txt /measure24/
RUN pip3 install -r requirements.txt

COPY . /measure24/

ADD ./start.sh /home/start.sh
RUN chmod +x /home/start.sh
