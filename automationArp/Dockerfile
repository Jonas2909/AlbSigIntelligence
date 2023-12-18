FROM alpine:latest
COPY my_test /bin/my_test
COPY root /var/spool/cron/crontabs/root
RUN chmod +x /bin/my_test
CMD crond -l 2 -f



RUN apk update
RUN apk add py-pip
RUN apk add --no-cache python3-dev
RUN apk add postgresql-dev gcc musl-dev
RUN pip install --upgrade pip
WORKDIR /app
COPY . /app
RUN pip --no-cache-dir install -r requirements.txt
CMD ["python3", "RestService.py"]
