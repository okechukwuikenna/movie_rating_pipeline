SELECT COUNT(*) AS total_rows FROM netflix;
SELECT * FROM netflix LIMIT 5;
SELECT type, COUNT(*) AS count_per_type FROM netflix GROUP BY type;
SELECT COUNT(*) AS missing_titles FROM netflix WHERE title IS NULL OR title = '';
SELECT rating, COUNT(*) AS count_per_rating FROM netflix GROUP BY rating;
SELECT AVG(release_year) AS avg_release_year FROM netflix;
