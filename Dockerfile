FROM python:3.11-alpine3.20

WORKDIR /service/app

# Copy requirements first for better caching
COPY requirements.txt /service/app/

# Install dependencies
RUN apk --no-cache add curl build-base npm && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apk del build-base

# Copy application code
ADD ./src/ /service/app/

# Expose ports
EXPOSE 8081 8000

ENV PYTHONUNBUFFERED=1

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=5 \
    CMD curl -s --fail http://localhost:8081/health || exit 1

CMD ["python3", "-u", "app.py"]