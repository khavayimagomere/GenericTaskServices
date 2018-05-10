FROM alpine:latest

COPY .   /var/app

RUN chmod +x /var/app/run.sh

WORKDIR /var/app/

RUN apk update && \
 apk add python3 postgresql-libs && \
 apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev curl && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps


EXPOSE 8080

EXPOSE 3000

WORKDIR /var/app/

CMD /var/app/run.sh