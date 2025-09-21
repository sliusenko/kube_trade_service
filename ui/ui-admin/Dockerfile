# ---------- build stage ----------
FROM node:20 AS builder
WORKDIR /app

# Виносимо окремо, щоб кешувались залежності
COPY package*.json ./
RUN npm ci

# Додаємо увесь код і збираємо Vite
COPY . .
RUN npm run build

# ---------- runtime stage ----------
FROM nginx:1.25
# Статичний білд Vite кладемо в дефолтну веб-директорію nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Опційно: здоров'я контейнера
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD \
  wget -qO- http://localhost:80/ || exit 1

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
