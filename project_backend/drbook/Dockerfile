FROM python:3.13-slim-bookworm

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    python3-dev \
    postgresql-client \
    pkg-config \
    gcc \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN <<EOF > req.txt
asgiref==3.8.1
Django==5.2.3
django-cors-headers==4.7.0
django-environ==0.12.0
djangorestframework==3.16.0
djangorestframework_simplejwt==5.5.0
PyJWT==2.9.0
python-dotenv==1.1.0
sqlparse==0.5.3
tzdata==2025.2
psycopg2-binary==2.9.10
EOF

RUN pip3 install --no-cache-dir -r req.txt


COPY . /app/ # Keep this to copy the rest of your application code

ENV DJANGO_SETTINGS_MODULE=drbook.settings \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]