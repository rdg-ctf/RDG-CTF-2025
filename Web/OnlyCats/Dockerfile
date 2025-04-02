FROM ubuntu:jammy

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y nginx python3-flask python3-flask-basicauth && \
    rm -rf /var/lib/apt/lists/*

ENV FLAG='rdg{af4cf13151aee7af4aa26b9bb817a079}'

RUN mkdir -p /var/www/onlycats/assets
WORKDIR /var/www/onlycats
COPY app/templates ./templates/
COPY app/app.py .
COPY cat.jpg assets/
COPY app/default.conf /etc/nginx/sites-enabled/default

RUN chmod -R 755 /var/www && \
    sed -i 's/^user www-data;/# user www-data;/' /etc/nginx/nginx.conf && \
    service nginx restart

EXPOSE 80

CMD service nginx start && \
    python3 /var/www/onlycats/app.py
