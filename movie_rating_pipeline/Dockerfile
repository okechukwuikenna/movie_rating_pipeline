FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Avoid Python output buffering
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        postgresql-client \
        cron \
        build-essential \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies first (Docker caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY scripts/ scripts/
COPY sql/ sql/
COPY data/ data/
COPY run_pipeline.sh .

# Copy cron job
COPY cronjob /etc/cron.d/run_pipeline_cron

# Ensure cron file has correct permissions and newline at the end
RUN chmod 0644 /etc/cron.d/run_pipeline_cron && \
    crontab /etc/cron.d/run_pipeline_cron

# Create a log file for cron
RUN touch /var/log/cron.log

# Start cron in the foreground
CMD ["sh", "-c", "cron && tail -f /var/log/cron.log"]

