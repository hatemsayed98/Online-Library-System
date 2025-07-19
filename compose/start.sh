#!/bin/bash
set -e

echo "Starting Online Library System..."

echo "Waiting for database..."
python -c "
import time
import psycopg2
import os
from urllib.parse import urlparse

url = urlparse(os.getenv('DATABASE_URL'))
for i in range(30):
    try:
        conn = psycopg2.connect(
            host=url.hostname,
            port=url.port or 5432,
            database=url.path[1:],
            user=url.username,
            password=url.password
        )
        conn.close()
        print('Database ready!')
        break
    except:
        print(f'Database not ready, waiting... ({i+1}/30)')
        time.sleep(2)
else:
    print('Database connection failed!')
    exit(1)
"

echo "Running migrations..."
flask db upgrade

echo "Starting Flask app..."
exec gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app
