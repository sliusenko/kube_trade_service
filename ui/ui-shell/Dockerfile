# ---------- build stage ----------
FROM node:20 AS builder
WORKDIR /app

# Copy package.json and package-lock.json first (better build cache)
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy project files and build the app
COPY . .
RUN npm run build

# ---------- runtime stage ----------
FROM nginx:1.25

# Default port (can be overridden at runtime via ENV)
ENV PORT=80

# Copy built frontend files to nginx web root
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx template config (supports envsubst for $PORT)
COPY default.conf.template /etc/nginx/templates/default.conf.template

# Expose default port (Kubernetes Service/Deployment will manage mapping)
EXPOSE 80

# Start nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
