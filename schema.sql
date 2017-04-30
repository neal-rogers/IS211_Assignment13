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

CREATE TABLE Results
(
    id int PRIMARY KEY,
    quizid int,
    studentid int,
    grade float
    );