FROM node:16

WORKDIR /app

COPY ./src/index.js /app/index.js
COPY ./src/package.json /app/package.json

RUN npm install

ENTRYPOINT [ "node", "index.js" ]