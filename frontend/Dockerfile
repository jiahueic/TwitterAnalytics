# Use an official Node.js runtime as the base image
FROM node:14-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the built Vue files into the container
COPY . .

# build app for production with minification
RUN npm run build

EXPOSE 8080
CMD [ "npx", "http-server", "dist" ]