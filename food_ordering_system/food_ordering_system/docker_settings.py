"""
Django settings for food_ordering_system project in Docker environment.
"""

import os
from pathlib import Path
from .settings import *  # Import all settings from the original settings file

# Override database settings for Docker
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'food_ordering_system'),
        'USER': os.environ.get('DB_USER', 'admin'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '123456'),
        'HOST': os.environ.get('DB_HOST', 'db'),  # Use the service name from docker-compose
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}

# Update CORS settings for Docker
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:8080",
    "http://backend:8000",
    "http://frontend:8080",
]

# Allow all hosts
ALLOWED_HOSTS = ['*']
