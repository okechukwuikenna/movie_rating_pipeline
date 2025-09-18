CREATE TABLE IF NOT EXISTS netflix (
    id SERIAL PRIMARY KEY,
    type VARCHAR(20) NOT NULL,
    title VARCHAR(255) NOT NULL,
    director VARCHAR(255),
    cast_list VARCHAR(500),
    release_year INT,
    rating VARCHAR(10),
    duration VARCHAR(50)
);
