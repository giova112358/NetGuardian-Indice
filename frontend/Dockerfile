# Build stage
FROM node:20-alpine AS build
WORKDIR /app
COPY frontend/package.json ./
# If you have a lock file, uncomment next line:
COPY frontend/package-lock.json ./
RUN npm install
COPY frontend /app
RUN npm run build

# Serve with nginx
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
# No CMD override needed (nginx default)