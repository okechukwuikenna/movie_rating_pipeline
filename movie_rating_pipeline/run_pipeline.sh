#!/bin/bash
set -e

echo "Starting pipeline..."

# Run combined ETL
python /app/scripts/preprocessing.py

# Run validation queries
psql "host=$DB_HOST port=$DB_PORT dbname=$DB_NAME user=$DB_USER password=$DB_PASS" <<EOF
SELECT COUNT(*) AS total_rows FROM netflix;
SELECT type, COUNT(*) FROM netflix GROUP BY type;
SELECT * FROM netflix LIMIT 5;
EOF

echo "Pipeline completed successfully!"
