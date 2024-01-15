FROM alpine:latest
RUN apk update
RUN apk add py-pip
RUN apk add --no-cache python3-dev
RUN apk add postgresql-dev gcc musl-dev
RUN pip install --upgrade pip --break-system-packages
WORKDIR /app
COPY ./Backend/RestService /app
RUN pip install --upgrade pip --break-system-packages
RUN pip --no-cache-dir install -r requirements.txt --break-system-packages
