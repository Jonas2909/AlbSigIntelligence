FROM alpine:latest
RUN apk update
RUN apk add py-pip
RUN apk add --no-cache python3-dev
RUN apk add postgresql-dev gcc musl-dev
RUN pip install --upgrade pip

WORKDIR /app

# Print the current directory and list its contents for debugging
RUN pwd && ls -la

COPY . /app

# Print the content of /app for debugging
RUN ls -la

RUN pip --no-cache-dir install -r requirements.txt
CMD ["python3", "RestService.py"]
