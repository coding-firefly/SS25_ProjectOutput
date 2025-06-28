FROM python:3.10-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-dev \
    postgresql-client \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY req.txt /app/

RUN pip3 install --no-cache-dir -r req.txt

COPY . /app/

ENV DJANGO_SETTINGS_MODULE=drbook.settings \
    PYTHONUNBUFFERED=1

EXPOSE 8000

#handle this in docker compose at entrypoint script at run time
#RUN python3 manage.py migrate

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

#WSGI
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project_name.wsgi"]
