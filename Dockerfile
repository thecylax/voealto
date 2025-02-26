# Stage 1: Build stage
FROM python:3.11-slim as builder

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=voealto.settings

WORKDIR /app

# Instale as dependências do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install dependencies in a virtual environment
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files
RUN /opt/venv/bin/python manage.py collectstatic --no-input

# Stage 2: Final stage
FROM python:3.11-slim

# Instale as dependências do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libcairo2 \
    libpango-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=voealto.settings

# Copy only the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application code
COPY --from=builder /app /app

# Set the working directory
WORKDIR /app

# Ensure the virtual environment is used
ENV PATH="/opt/venv/bin:$PATH"

# Expose the port the app runs on
EXPOSE 8000

# Run the application using gunicorn
# RUN ls -l
# CMD ["gunicorn", "voealto.wsgi:application", "--bind", "0.0.0.0:8000", "--pythonpath", "/app"]
