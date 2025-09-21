# ./ginx-core/Dockerfile
ARG BASE_VERSION=stable-alpine3.20
FROM nginx:${BASE_VERSION}

ENV LANGUAGE=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LC_CTYPE=en_US.UTF-8

# інструменти: dig (bind-tools), curl, модуль njs
RUN apk update && apk upgrade && \
    apk add --no-cache bash curl bind-tools nginx-module-njs && \
    rm -rf /var/cache/apk/*

# Директорії для статичних сторінок (опціонально)
RUN mkdir -p /etc/nginx/mainepage \
             /etc/nginx/scheduled_mainpage \
             /etc/nginx/zest4iot_mainpage

# Сторінки (заміни своїми, якщо треба)
COPY ./mainpage/index.html            /etc/nginx/mainpage/index.html
COPY ./scheduled_mainpage/index.html  /etc/nginx/scheduled_mainpage/index.html
COPY ./zest4iot_mainpage/             /etc/nginx/zest4iot_mainpage/

# Скрипт моніторингу DNS і reload NGINX
COPY ./reload.sh /usr/local/bin/reload.sh
RUN chmod +x /usr/local/bin/reload.sh

# Порти
EXPOSE 80

# Запуск: стартує nginx (в бекграунді) і моніторить DNS у циклі
CMD ["bash", "/usr/local/bin/reload.sh"]
