DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS choices CASCADE;
DROP TABLE IF EXISTS drinks CASCADE;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE CHECK(username IS NOT NULL AND length(username) > 2),
    password TEXT CHECK(password IS NOT NULL AND length(password) > 7)
);

CREATE TABLE IF NOT EXISTS choices (
    id SERIAL PRIMARY KEY,
    drink_name TEXT,
    alcohol_content INTEGER
);

CREATE TABLE IF NOT EXISTS drinks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    drink_id INTEGER REFERENCES choices,
    drink_time TIMESTAMP
);

INSERT INTO choices (drink_name, alcohol_content) VALUES ('Beer', 12);
INSERT INTO choices (drink_name, alcohol_content) VALUES ('Wine', 12);
INSERT INTO choices (drink_name, alcohol_content) VALUES ('Kossu', 12);