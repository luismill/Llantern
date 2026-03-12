# Stage 1: Build the Svelte application
FROM node:20-alpine as build

WORKDIR /app

COPY package.json ./
# Since we didn't use package-lock.json to avoid prompts, we just run npm install
RUN npm install

COPY . .

# Build the application
RUN npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:alpine

# Copy the built assets from the build stage to Nginx's default public directory
COPY --from=build /app/dist /usr/share/nginx/html

# Replace default Nginx configuration to enable SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
