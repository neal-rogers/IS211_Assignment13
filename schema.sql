CREATE TABLE Students
(
    id int PRIMARY KEY,
    firstname text,
    lastname text
    );

CREATE TABLE Quizzes
(
    id int PRIMARY KEY,
    subject text,
    questions int,
    qdate date
    );

CREATE TABLE Results
(
    id int PRIMARY KEY,
    quizid int,
    studentid int,
    grade float
    );