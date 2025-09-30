# ---------- build stage ----------
FROM node:20 AS builder
WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .
RUN npm run build

# ---------- runtime stage ----------
FROM nginx:1.25

RUN apt-get update && apt-get install -y gettext-base wget && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/dist /usr/share/nginx/html

COPY default.conf.template /etc/nginx/templates/default.conf.template

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PORT=8080

ENTRYPOINT ["/entrypoint.sh"]

CMD ["sh", "-c", ": \"${PORT:=8080}\"; \
  envsubst '$PORT' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf && \
  exec nginx -g 'daemon off;'"]

EXPOSE 8080

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -qO- "http://localhost:${PORT:-8080}/" || exit 1
