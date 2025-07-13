FROM python:3.10-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    python3-dev \
    postgresql-client \
    pkg-config \
    gcc \
    curl \
    tar \
    autoconf \
    automake \
    libtool \
    && rm -rf /var/lib/apt/lists/*

ENV SQLITE_VERSION=3.46.0 # Use a very recent stable version, e.g., from sqlite.org/download.html
ENV SQLITE_TARBALL=sqlite-autoconf-${SQLITE_VERSION//./}00.tar.gz # This filename pattern is generally correct

ENV LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH" # Ensure Python finds the new SQLite

WORKDIR /tmp
RUN curl -fsSL https://www.sqlite.org/src/$SQLITE_TARBALL -o $SQLITE_TARBALL && \
    tar -xvf $SQLITE_TARBALL && \
    cd sqlite-autoconf-${SQLITE_VERSION//./}00 && \
    ./configure --prefix=/usr/local && \
    make -j$(nproc) && \
    make install && \
    ldconfig && \
    cd .. && \
    rm -rf sqlite-autoconf* $SQLITE_TARBALL


WORKDIR /app # Return to your application directory

COPY req.txt /app/
RUN pip3 install --no-cache-dir -r req.txt

COPY . /app/

ENV DJANGO_SETTINGS_MODULE=drbook.settings \
    PYTHONUNBUFFERED=1

EXPOSE 8000


CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]