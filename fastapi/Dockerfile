FROM python:3.10-slim-bullseye

RUN apt-get update -qqy && \
    apt-get -qqy --no-install-recommends install sudo build-essential wget && \
    apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false

RUN adduser appuser
RUN echo "appuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER appuser
WORKDIR /home/appuser

COPY --chown=appuser:appuser requirements.txt requirements.txt

RUN python -m venv venv
RUN venv/bin/pip install pip wheel setuptools --upgrade
RUN venv/bin/pip install -r requirements.txt && rm -rf ~/.cache/pip

COPY --chown=appuser:appuser app app
COPY --chown=appuser:appuser entrypoints/server-entrypoint.sh ./
COPY --chown=appuser:appuser entrypoints/testing-entrypoint.sh ./

RUN chmod +x server-entrypoint.sh
RUN chmod +x testing-entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["./server-entrypoint.sh"]
