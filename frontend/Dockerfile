# Stage 1: Build an Angular Docker Image
FROM node:14.15 as Build

COPY package*.json /app/
RUN npm install

WORKDIR /app
COPY . /app

RUN npm install
RUN npm install -g @angular/cli
RUN npm install --save-dev @angular-devkit/build-angular

CMD ng serve --host 0.0.0.0
EXPOSE 4200/tcp