FROM alpine

RUN apk add --update openssh python3 net-snmp net-snmp-tools sudo

RUN addgroup -S eccm

COPY ./src /emul
RUN adduser -s /bin/sh -h /emul -D admin \
    && echo admin:password | chpasswd \
    && echo "admin ALL=(ALL) NOPASSWD: ALL" | sudo EDITOR='tee -a' visudo

RUN chmod -R 2777 /emul

CMD ["sh", "/emul/start.sh"]