DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Quiz;
DROP TABLE IF EXISTS Results;

CREATE TABLE Students
(
    firstname text PRIMARY KEY,
    lastname text
    );

CREATE TABLE Quiz
(
    id int PRIMARY KEY,
    subject text,
    questions int,
    qdate date
    );

CREATE TABLE Songs
(
    song_id int PRIMARY KEY,
    song_title varchar NOT NULL
    album_id int NOT NULL REFERENCES Albums(album_id)
    artist_id int NOT NULL REFERENCES Artist(artist_id)
    track_number int NOT NULL
    track_length varchar
    );