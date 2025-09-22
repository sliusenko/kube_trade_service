FROM node:20 AS builder
WORKDIR /app

# Cache deps
COPY package*.json ./
RUN npm ci

# Build Vite assets
COPY . .
RUN npm run build

# ---------- runtime stage ----------
FROM nginx:1.25

# Install envsubst for templating
RUN apt-get update && apt-get install -y gettext-base && rm -rf /var/lib/apt/lists/*

# Copy built static files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx template (uses $PORT)
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

# Default PORT (can be overridden by Deployment/Helm)
ENV PORT=8080

# Generate final nginx config from template and start nginx
# NOTE: envsubst *variable list* must use literal names (e.g. '$PORT'), not values.
CMD sh -c ': "${PORT:=8080}"; \
  envsubst '\''$PORT'\'' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf && \
  exec nginx -g "daemon off;"'

# Optional: container metadata
EXPOSE 8080

# Healthcheck uses the resolved PORT at runtime
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD wget -qO- "http://localhost:${PORT:-8080}/" || exit 1
