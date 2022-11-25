# Stage 1: Build an Angular Docker Image
FROM node:14.20 as Build

WORKDIR /app
COPY package*.json /app/
RUN npm install --no-package-lock
COPY . /app
CMD npm run start
EXPOSE 4200/tcp
