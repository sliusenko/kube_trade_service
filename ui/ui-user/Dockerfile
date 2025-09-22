# ---------- build stage ----------
FROM node:20 AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# ---------- runtime stage ----------
FROM nginx:1.25

ENV PORT=80

COPY --from=builder /app/dist /usr/share/nginx/html

COPY default.conf.template /etc/nginx/templates/default.conf.template

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

