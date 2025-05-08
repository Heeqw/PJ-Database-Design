FROM python:3.11-slim

WORKDIR /app

# Install system dependencies with retry logic
RUN apt-get update && \
    # Add retry logic for apt-get
    for i in $(seq 1 3); do \
        apt-get install -y \
        default-libmysqlclient-dev \
        build-essential \
        pkg-config \
        curl \
        wget && break || \
        if [ $i -lt 3 ]; then \
            echo "apt-get attempt $i failed, retrying..." && \
            sleep 5 && \
            apt-get update; \
        else \
            echo "apt-get failed after 3 attempts" && \
            exit 1; \
        fi; \
    done && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies with retry logic
RUN for i in $(seq 1 3); do \
        pip install --no-cache-dir -r requirements.txt && break || \
        if [ $i -lt 3 ]; then \
            echo "pip install attempt $i failed, retrying..." && \
            sleep 5; \
        else \
            echo "pip install failed after 3 attempts" && \
            exit 1; \
        fi; \
    done

# Copy project files
COPY . .

# Copy entrypoint script
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
