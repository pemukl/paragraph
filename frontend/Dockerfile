FROM node:20-alpine

WORKDIR /usr/src/app

COPY package*.json ./
COPY vite.config.js ./vite.config.js
COPY svelte.config.js ./svelte.config.js

RUN npm install

COPY ./src ./src

RUN npm run build

COPY ./data ./data

EXPOSE 4173

ENV HOST=0.0.0.0

CMD [ "npm", "run", "preview" ]