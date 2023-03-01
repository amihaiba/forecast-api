# syntax=docker/dockerfile:1
FROM nginx:alpine
RUN ["rm","/etc/nginx/conf.d/default.conf"]
COPY default.conf /etc/nginx/conf.d/default.conf
COPY nginx-certificate.crt /etc/nginx/certificate/nginx-certificate.crt
COPY nginx.key /etc/nginx/certificate/nginx.key
