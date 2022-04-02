FROM python:3.7-alpine

WORKDIR /api

COPY setup.py .
COPY setup.cfg .

RUN pip install --no-cache-dir --upgrade -e '.[dev]'

COPY . .

CMD ["python3", "-m", "run"]
