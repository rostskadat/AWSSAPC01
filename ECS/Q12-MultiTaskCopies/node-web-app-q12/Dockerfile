FROM node:12

LABEL Architecture and Emerging Technologies "architectureemergingtechnologies@allfunds.com"

ARG USE_PROXY=false

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

RUN if ($USE_PROXY); then \
    npm config set proxy http://afb1linjk01p.prod.allfunds.bank:80 ; \
    npm config set https-proxy http://afb1linjk01p.prod.allfunds.bank:80 ; \
    fi; \
    npm install
# If you are building your code for production
# RUN npm ci --only=production

# Bundle app source
COPY . .

EXPOSE 8080

CMD [ "node", "server.js" ]