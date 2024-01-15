FROM node:16-alpine as buildFrontEnd
WORKDIR /app
ENV PATH /node_modules/.bin:$PATH
COPY ./Frontend/albsigintelligence/package.json .
COPY ./Frontend/albsigintelligence/package-lock.json .
RUN npm ci --force
RUN npm install react-scripts@4.0.1 -g
COPY ./Frontend/albsigintelligence /app
RUN ls -al
RUN npm run build

FROM nginx:1.19.0
COPY ./Frontend/albsigintelligence/cert.pem /etc/nginx/ssl/cert.pem
COPY ./Frontend/albsigintelligence/key.pem /etc/nginx/ssl/key.pem
COPY ./Frontend/albsigintelligence/nginx.conf /etc/nginx/nginx.conf
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=buildFrontEnd /app/build .
