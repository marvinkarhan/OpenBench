#!/usr/bin/env sh
set -e

# Wait for MySQL to be ready
echo "Waiting for MySQL at ${MYSQL_HOST}:${MYSQL_PORT}..."
until nc -z ${MYSQL_HOST:-db} ${MYSQL_PORT:-3306}; do
  sleep 1
done

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000

