CREATE SCHEMA IF NOT EXISTS stg;

DROP TABLE IF EXISTS stg.posts;

CREATE TABLE stg.posts (
    user_id INT,
    id INT,
    title VARCHAR(255),
    body TEXT,
    load_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);