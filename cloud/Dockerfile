FROM python:2.7
RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN /bin/bash -c '[ -f requirements-prod.txt ] && pip install -r requirements.txt'
