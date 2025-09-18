
# Movie Ratings Data Pipeline

## Project Overview

The **Movie Ratings Data Pipeline** ingests raw movie and TV show data, cleans and transforms it, and loads it into a PostgreSQL database. The pipeline is automated to run on a schedule using Docker and cron.  

This allows the product team at JordanStream to analyze customer preferences and improve recommendation systems.  

---

## Features

- Loads raw dataset: `netflix_titles.csv`  
- Cleans and standardizes data:
  - Handles missing values
  - Formats dates, numbers, and durations
  - Strips whitespace
- Creates PostgreSQL table automatically if it doesn’t exist
- Inserts cleaned data into PostgreSQL
- Runs validation queries:
  - Total rows
  - Counts by type (Movie / TV Show)
  - Preview of first 5 rows
- Automated execution via cron every 10 minutes
- Fully containerized using Docker and Docker Compose

---

## Directory Structure

```text
movie_rating_pipeline/
├─ data/
│  └─ netflix_titles.csv
├─ scripts/
│  └─ preprocessing.py   # Combined preprocessing + DB load
├─ sql/
│  ├─ create_tables.sql
│  └─ queries.sql
├─ run_pipeline.sh
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
├─ cronjob
└─ README.md
````

---

## Prerequisites

* Ubuntu / WSL
* Docker
* Docker Compose
* Python 3.10+ (inside Docker container)
* PostgreSQL client (inside Docker container)

---

## Setup Instructions

### 1. Navigate to project directory

```bash
cd /mnt/c/Users/IOkechukwu/movie_rating_pipeline
```

### 2. Build Docker containers

```bash
docker compose build
```

### 3. Start containers

```bash
docker compose up -d
```

**Containers:**

* `db`: PostgreSQL database
* `python_container`: Python container with preprocessing and cron

---

### Manual Pipeline Execution

To run the preprocessing pipeline manually:

```bash
docker exec -it python_container ./run_pipeline.sh
```

Check logs:

```bash
docker exec -it python_container cat /app/pipeline.log
```

Check database:

```bash
docker exec -it db psql -U iokechukwu -d data_engineering
```

---

### Automatic Pipeline (Cron)

* Cron runs inside the Python container every 10 minutes (configured in `cronjob`).
* Pipeline logs are written to `/app/pipeline.log` inside the container.

---

### Notes

* The preprocessing script `preprocessing.py` handles both preprocessing and loading to the database.
* Table creation is automatic; no need to run `create_tables.sql`.
* Validation queries are included in `run_pipeline.sh` to verify data integrity.

---

### License

This project is for internal use at JordanStream and educational purposes.

N/B. I starred the password for security reasons

```



