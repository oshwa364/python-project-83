DROP TABLE IF EXISTS urls CASCADE;
DROP TABLE IF EXISTS url_checks CASCADE;

CREATE TABLE IF NOT EXISTS urls (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS url_checks (
    id SERIAL PRIMARY KEY,
    url_id INTEGER REFERENCES urls(id),
    status_code INTEGER,
    h1 VARCHAR(255),
    title VARCHAR(255),
    description VARCHAR(255),
    created_at TIMESTAMP
);