# ---- Build stage: compile the React app with Vite ----
FROM node:22-alpine AS build
WORKDIR /app

# Install deps first (cached unless package files change)
COPY package*.json ./
RUN npm ci

# Vite bakes VITE_* vars at BUILD time, so they must be present now.
# Passed from docker-compose build args.
ARG VITE_API_BASE_URL=http://localhost:8000
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

COPY . .
RUN npm run build

# ---- Serve stage: static files via nginx ----
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
