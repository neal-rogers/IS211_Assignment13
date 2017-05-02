drop table if exists Students;
drop table if exists Quizzes;
drop table if exists Results;

CREATE TABLE Students (
    id integer PRIMARY KEY autoincrement,
    firstname text not null,
    lastname text not null
    );

CREATE TABLE Quizzes (
    id integer PRIMARY KEY autoincrement,
    subject text not null,
    questions integer not null,
    qdate date not null
    );

CREATE TABLE Results (
    id integer PRIMARY KEY autoincrement,
    quizid integer,
    studentid int,
    grade float
    );

INSERT INTO Students VALUES(Null, 'John', 'Smith');
INSERT INTO Quizzes VALUES(Null,'Python Basics', 5, '2/05/2015');
INSERT INTO Results VALUES(Null,(select ID from Quizzes where subject = 'Python Basics'),(select ID from Students where firstName = 'John' and lastName = 'Smith'),85;