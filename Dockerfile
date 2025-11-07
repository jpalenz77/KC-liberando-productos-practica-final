FROM python:3.11-alpine3.20

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN apk --no-cache add curl build-base && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apk del build-base

# Copy application code
COPY src/ .

# Expose ports
EXPOSE 8081

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=5 \
    CMD curl -s --fail http://localhost:8081/health || exit 1

# Run the application
CMD ["python3", "-u", "application/app.py"]