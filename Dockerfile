FROM python:3.7.1-alpine3.8

RUN set -eux && \
    apk --update add --no-cache dumb-init libffi-dev openssl-dev && \
    pip install --no-cache-dir virtualenv

COPY . /app
RUN virtualenv /env && \
    apk --update add --no-cache --virtual .build-deps build-base && \
    /env/bin/pip install --no-cache-dir /app && \
    apk del .build-deps

USER nobody
ENV PATH=/env/bin:${PATH}
WORKDIR /app

CMD ["gdg-pisa-user-manager"]
