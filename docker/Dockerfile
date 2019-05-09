FROM python:3.7.2-alpine3.7

LABEL maintainer="michele.sacchetti@gmail.com"

WORKDIR /tmp
COPY . .

RUN \
  mkdir -p /tmp/wheels && \
  apk add gcc musl-dev python3-dev libffi-dev openssl-dev && \
  pip wheel urllib3==1.24.3 click==7.0 schedule==0.5.0 kubernetes==7.0.0 python-consul==1.1.0 sphinx==1.8.2 sphinx-rtd-theme==0.4.2 sphinx-click==1.4.1 \
  --wheel-dir=/tmp/wheels --no-cache-dir && \
  python3 setup.py sdist bdist_wheel && \
  mv dist/*.whl /tmp/wheels


FROM python:3.7.2-alpine3.7
LABEL maintainer="michele.sacchetti@gmail.com"

ENV CM2C_INTERVAL="5" \
  CM2C_LOG_LEVEL="info" \
  CM2C_NAMESPACE="default" \
  CM2C_LABEL_SELECTOR="" \
  CM2C_CONSUL_URL="http://localhost:8500" \
  CM2C_CONSUL_PATH="test" \
  CM2C_MODE="spring"

COPY --from=0 /tmp/wheels/* /tmp/
ADD ./docker/entrypoint.sh /entrypoint.sh

RUN \
  pip uninstall urllib3 && \
  pip install --no-index --no-cache-dir --find-links=/tmp click schedule kubernetes python-consul configmap2consul && \
  rm -rf /tmp/*

CMD [ "sh", "/entrypoint.sh" ]
