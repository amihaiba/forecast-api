# syntax=docker/dockerfile:1
# Base image
FROM python:3.8.16-slim
# Set app directory
WORKDIR /usr/share/forecast-api
RUN useradd -r -g users user && chown user:users /usr/share/forecast-api
ADD --chown=user:users requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN mkdir history && chown user:users history
# Create a system user and change app ownership
# Expose app port and set entrypoint to start a gunicorn WSGI server
EXPOSE 5000
ENTRYPOINT ["gunicorn","--user","user","--workers","1","--umask","007","--bind","0.0.0.0:5000","wsgi:app"]
# Copy application files
ADD --chown=user:users . .
# Switch user
USER user
# Set environment variables
ENV BG_COLOR="primary" \
    APP_PATH="forecast-api"
