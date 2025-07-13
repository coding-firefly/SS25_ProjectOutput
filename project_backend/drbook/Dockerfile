FROM python:3.13-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    default-libmysqlclient-dev \
    python3-dev \
    libsqlite3-dev \
    postgresql-client \
    curl \
    tar \
    wget \
    autoconf \
    automake \
    libtool \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY req.txt /app/
RUN pip3 install --no-cache-dir -r req.txt

COPY . /app/

ENV DJANGO_SETTINGS_MODULE=drbook.settings \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
