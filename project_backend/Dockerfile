FROM python:3.7-slim

WORKDIR /api

COPY setup.py .
COPY setup.cfg .

RUN apt-get -y update && apt-get install -y default-libmysqlclient-dev python3-dev gcc
RUN pip install --no-cache-dir --upgrade -e '.[dev]'

COPY . .

CMD ["python3", "-m", "run"]
