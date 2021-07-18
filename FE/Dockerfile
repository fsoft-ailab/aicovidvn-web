FROM node:lts-alpine as builder

# make the 'app' folder the current working directory
WORKDIR /app

# copy both 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

# build app for production with minification
RUN npm run build

FROM node:lts-alpine

# make the 'app' folder the current working directory
WORKDIR /app

COPY --from=builder /app/dist /app/dist
COPY --from=builder /app/server.js /app/server.js 

# install express
RUN npm install --save express

EXPOSE 8080

CMD [ "node", "server.js" ]