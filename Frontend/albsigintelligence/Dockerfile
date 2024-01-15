FROM node:16-alpine as buildFrontEnd
WORKDIR /app
ENV PATH /node_modules/.bin:$PATH
COPY package.json .
COPY package-lock.json .
RUN npm ci --force
RUN npm install react-scripts@4.0.1 -g
COPY . .
RUN npm run build

FROM nginx:1.19.0
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=buildFrontEnd /app/build .
ENTRYPOINT [ "nginx", "-g", "daemon off;" ]