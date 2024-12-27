FROM php:8-apache

RUN echo "CYHUNT24{REDACTED}" > /flag.txt
RUN chmod 444 /flag.txt

RUN apt update

WORKDIR /var/www/html

ADD index.php ./
ADD admin.php ./
RUN chown -R root:www-data ./
RUN chmod -R 440           ./
RUN chmod    550           ./