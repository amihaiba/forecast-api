# syntax=docker/dockerfile:1
FROM ubuntu:20.04

LABEL "ws"="Containers - Docker"
LABEL "exercise"="24"

RUN apt-get update && apt-get -y upgrade && apt-get install -y python3 \
&& apt-get install -y python3-pip

WORKDIR /usr/src/forecast_api
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
RUN useradd -r -g users user

USER user

ENTRYPOINT ["gunicorn","--user","user","--workers","3","--umask","007","--bind","0.0.0.0:5000","wsgi:app"]
