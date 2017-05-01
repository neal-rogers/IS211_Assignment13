#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This program does stuff."""

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

USERNAME = 'admin'
PASSWORD = 'password'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['hw13.db'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/dashboard')
def show_entries():
    cur1 = g.db.execute('select id, firstname, lastname from Students')
    students = [dict(firstname=row[1], lastname=row[1]) for row in cur1.fetchall()]
    cur2 = g.db.execute('select id, subject, questions, qdate from Quizzes')
    cur2 = g.db.execute('select ID, subject, questions, testDate from Quizzes')
    quizzes = [dict(subject=row[1], questions=row[2], qate=row[3])
               for row in cur2.fetchall()]
    return render_template('show_entries.html', students=students, quizzes=quizzes)

@app.route('/student/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into Students (firstname, lastname) values (?, ?)',
                 [request.form['firstname'], request.form['lastname']])
    g.db.commit()
    flash('New student record was successfully added.')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()