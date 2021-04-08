FROM python:3.9.4-alpine3.13

# install depencencies
RUN set -eux && \
    apk --update add --no-cache dumb-init libffi-dev openssl-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir virtualenv

# copy the app
COPY . /app
WORKDIR /app

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

# install the module inside a venv
RUN virtualenv /venv && \
    apk --update add --no-cache --virtual .build-deps build-base && \
    /venv/bin/pip install --no-cache-dir /app && \
    apk del .build-deps

# add the module to path
ENV PATH=/venv/bin:${PATH}

# run without privileges
USER nobody

# start
CMD ["gdg-pisa-user-manager"]
