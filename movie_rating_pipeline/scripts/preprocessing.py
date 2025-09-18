import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os

# Database credentials
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = int(os.environ.get("DB_PORT", 5432))
DB_NAME = os.environ.get("DB_NAME", "data_engineering")
DB_USER = os.environ.get("DB_USER", "iokechukwu")
DB_PASS = os.environ.get("DB_PASS", "ikenna004")

# 1. Load raw CSV
df = pd.read_csv("data/netflix_titles.csv")

# 2. Preprocess
def preprocessing(df):
    df = df[['type', 'title', 'director', 'cast', 'release_year', 'rating', 'duration']].copy()
    df['type'] = df['type'].fillna('Unknown')
    df['director'] = df['director'].fillna('Unknown')
    df['cast'] = df['cast'].fillna('Unknown')
    df['rating'] = df['rating'].fillna('NR')
    df['duration'] = df['duration'].fillna('0 min')
    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')

    def format_duration(row):
        d = str(row['duration']).strip()
        if row['type'] == 'TV Show':
            return d if 'Season' in d else f"{d} Seasons"
        else:
            return d if 'min' in d else f"{d} min"

    df['duration'] = df.apply(format_duration, axis=1)
    for col in ['title', 'director', 'cast', 'rating', 'type']:
        df[col] = df[col].str.strip()

    df = df.rename(columns={'cast': 'cast_list'})
    return df

df_cleaned = preprocessing(df)

# Optional: save cleaned CSV
df_cleaned.to_csv("data/netflix_titles_clean.csv", index=False)

# 3. Connect to PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cursor = conn.cursor()

# 4. Create table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS netflix (
    id SERIAL PRIMARY KEY,
    type VARCHAR(20) NOT NULL,
    title VARCHAR(255) NOT NULL,
    director VARCHAR(255),
    cast_list TEXT,
    release_year INT,
    rating VARCHAR(10),
    duration VARCHAR(50)
);
"""
cursor.execute(create_table_query)
conn.commit()

# 5. Insert cleaned data
insert_query = """
INSERT INTO netflix (type, title, director, cast_list, release_year, rating, duration)
VALUES %s
"""
data_tuples = [tuple(x) for x in df_cleaned[['type', 'title', 'director', 'cast_list', 'release_year', 'rating', 'duration']].to_numpy()]
execute_values(cursor, insert_query, data_tuples)
conn.commit()

cursor.close()
conn.close()

print("Data preprocessing and insertion completed successfully!")
