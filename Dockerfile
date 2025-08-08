FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps for mysqlclient
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev build-essential netcat-openbsd pkg-config \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static not needed for dev; migrations run in entrypoint

COPY ./docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

