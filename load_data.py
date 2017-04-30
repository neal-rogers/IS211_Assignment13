#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This program loads and inserts values into a database."""

import sqlite3 as lite
import sys


con = lite.connect('hw13.db')

Students = (
    (1, 'John','Smith')
)

Quizzes = (
    (1, 'Python Basics', 5, '02/05/2015')
)

Results = (
    (1, 1, 1, 85)
)

with con:
    cur = con.cursor()
    cur.executemany('INSERT INTO Students VALUES(?, ?, ?)', Students)
    cur.executemany('INSERT INTO Quizzes VALUES(?, ?, ?, ?)', Quizzes)
    cur.executemany('INSERT INTO Results VALUES(?, ?, ?, ?)', Results)