FROM python:3.7-alpine

WORKDIR /api

COPY setup.py .
COPY setup.cfg .

RUN apk update && apk add gcc python3-dev build-base openssl-dev libffi-dev
RUN pip install pymysql
RUN pip install cryptography
RUN pip install --no-cache-dir --upgrade -e '.[dev]'

COPY . .

CMD ["python3", "-m", "run"]
