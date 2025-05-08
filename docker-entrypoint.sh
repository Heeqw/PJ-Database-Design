#!/bin/bash
set -e

# Wait for database to be ready
echo "Waiting for database to be ready..."
python -c "
import sys
import time
import MySQLdb

# Try up to 30 times, waiting 2 seconds between attempts
for i in range(30):
    try:
        MySQLdb.connect(
            host='db',
            user='admin',
            passwd='123456',
            db='food_ordering_system',
            port=3306
        )
        print('Database connection successful')
        sys.exit(0)
    except MySQLdb.OperationalError:
        print(f'Database connection attempt {i+1} failed, retrying in 2 seconds...')
        time.sleep(2)

print('Could not connect to database after 30 attempts')
sys.exit(1)
"

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Always initialize data to ensure all required data is present
echo "Initializing data..."
python manage.py initialize_data

# Start application
echo "Starting application..."
exec "$@"
