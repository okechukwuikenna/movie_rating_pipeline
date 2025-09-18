FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y postgresql-client cron && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/ scripts/
COPY sql/ sql/
COPY data/ data/
COPY run_pipeline.sh .
COPY cronjob /etc/cron.d/run_pipeline_cron
COPY wait-for.sh /app/wait-for.sh

RUN chmod +x run_pipeline.sh /app/wait-for.sh && \
    chmod 0644 /etc/cron.d/run_pipeline_cron && \
    crontab /etc/cron.d/run_pipeline_cron

CMD ["cron", "-f"]
