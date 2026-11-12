FROM node:20-alpine AS builder

WORKDIR /app

ARG VITE_BASE_PATH=/
ARG VITE_API_URL=/api/v1

ENV VITE_BASE_PATH=$VITE_BASE_PATH
ENV VITE_API_URL=$VITE_API_URL

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build:prod

FROM nginx:alpine

# nginx.conf serves the app under /devotional-journal/ (public deployment);
# nginx.mesh.conf serves it at the root of its own host name (private mesh).
ARG NGINX_CONF=nginx.conf

COPY --from=builder /app/dist /usr/share/nginx/html
COPY ${NGINX_CONF} /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
