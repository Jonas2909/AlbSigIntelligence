FROM alpine:latest
RUN apk update
RUN apk add curl
RUN apk add arp-scan
COPY automationArp /bin/automationArp
COPY root /var/spool/cron/crontabs/root
RUN chmod +x /bin/automationArp
CMD crond -l 2 -f
