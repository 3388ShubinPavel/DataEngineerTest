CREATE SCHEMA IF NOT EXISTS dds;

-- Hub User
CREATE TABLE IF NOT EXISTS dds.hub_user (
    hk_user_id VARCHAR(32) PRIMARY KEY, -- MD5 Hash
    user_id INT NOT NULL,               -- Бизнес-ключ
    load_dt TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL
);

-- Hub Post
CREATE TABLE IF NOT EXISTS dds.hub_post (
    hk_post_id VARCHAR(32) PRIMARY KEY, -- MD5 Hash
    post_id INT NOT NULL,               -- Бизнес-ключ
    load_dt TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL
);

-- Link User Post
CREATE TABLE IF NOT EXISTS dds.link_user_post (
    hk_user_post VARCHAR(32) PRIMARY KEY,
    hk_user_id VARCHAR(32) REFERENCES dds.hub_user(hk_user_id),
    hk_post_id VARCHAR(32) REFERENCES dds.hub_post(hk_post_id),
    load_dt TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL
);

-- Satellite Post
CREATE TABLE IF NOT EXISTS dds.sat_post (
    hk_post_id VARCHAR(32) REFERENCES dds.hub_post(hk_post_id),
    load_dt TIMESTAMP NOT NULL,
    hash_diff VARCHAR(32) NOT NULL, -- MD5 Hash от атрибутов (title, body)
    title VARCHAR(255),
    body TEXT,
    record_source VARCHAR(50) NOT NULL,
    PRIMARY KEY (hk_post_id, load_dt)
);