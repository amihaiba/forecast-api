# syntax=docker/dockerfile:1
FROM python:3.8.16-slim

WORKDIR /usr/src/forecast_api
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
RUN useradd -r -g users user

USER user

ENTRYPOINT ["gunicorn","--user","user","--workers","3","--umask","007","--bind","0.0.0.0:5000","wsgi:app"]
