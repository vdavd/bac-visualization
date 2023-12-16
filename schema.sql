DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS choices CASCADE;
DROP TABLE IF EXISTS drinks CASCADE;
DROP TABLE IF EXISTS rooms CASCADE;
DROP TABLE IF EXISTS members CASCADE;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE CHECK(username IS NOT NULL AND length(username) > 2),
    password TEXT CHECK(password IS NOT NULL AND length(password) > 7),
    user_weight INTEGER,
    user_height INTEGER,
    user_age INTEGER,
    sex TEXT
);

CREATE TABLE IF NOT EXISTS choices (
    id SERIAL PRIMARY KEY,
    drink_name TEXT,
    category TEXT,
    alcohol_content FLOAT
);

CREATE TABLE IF NOT EXISTS drinks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    drink_id INTEGER REFERENCES choices,
    drink_time TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rooms (
    id SERIAL PRIMARY KEY,
    owner_id INTEGER REFERENCES users,
    room_name TEXT UNIQUE CHECK(room_name IS NOT NULL AND length(room_name) > 2)
);

CREATE TABLE IF NOT EXISTS members (
    id SERIAL PRIMARY KEY,
    room_id INTEGER REFERENCES rooms,
    member_id INTEGER REFERENCES users,
    UNIQUE (room_id, member_id)
);

INSERT INTO choices (drink_name, category, alcohol_content) VALUES ('Beer 4.7%, 0.33l', 'Beer', 12.2);
INSERT INTO choices (drink_name, category, alcohol_content) VALUES ('Beer 5.2%, 0.33l', 'Beer', 13.5);
INSERT INTO choices (drink_name, category, alcohol_content) VALUES ('Beer 4.7%, 0.5l', 'Beer', 18.5);
INSERT INTO choices (drink_name, category, alcohol_content) VALUES ('Beer 5.2%, 0.5l', 'Beer', 20.5);
INSERT INTO choices (drink_name, category, alcohol_content) VALUES ('Wine 12%, 12cl', 'Wine', 11.4);
INSERT INTO choices (drink_name, category, alcohol_content) VALUES ('Wine 12%, 16cl', 'Wine', 15.1);
INSERT INTO choices (drink_name, category, alcohol_content) VALUES ('Wine 12%, 24cl', 'Wine', 22.7);
INSERT INTO choices (drink_name, category, alcohol_content) VALUES ('Liquor 38%, 4cl', 'Liquor', 12);
INSERT INTO choices (drink_name, category, alcohol_content) VALUES ('Liquor 38%, 2cl', 'Liquor', 6);
INSERT INTO choices (drink_name, category, alcohol_content) VALUES ('Liquor 40%, 4cl', 'Liquor', 12.6);
INSERT INTO choices (drink_name, category, alcohol_content) VALUES ('Liquor 40%, 2cl', 'Liquor', 6.3);
INSERT INTO choices (drink_name, category, alcohol_content) VALUES ('Desi 38%', 'Liquor', 30);