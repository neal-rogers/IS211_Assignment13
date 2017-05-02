#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This program does stuff."""

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing


# configuration
DATABASE = 'hw13.db'
USERNAME = 'admin'
PASSWORD = 'password'
DEBUG = False
SECRET_KEY = 'devkey123'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

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
    db = getattr(g, 'hw13', None)
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

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/dashboard')
def show_entries():
    cur1 = g.db.execute('select id, firstname, lastname from Students')
    students = [dict(firstname=row[1], lastname=row[1]) for row in cur1.fetchall()]
    cur2 = g.db.execute('select id, firstname, lastname from Students')
    cur2 = g.db.execute('select id, subject, questions, qdate from Quizzes')
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

@app.route('/student/<id>')
def student_results(id):
     msg = None
     cur = g.db.execute('select quiz, grade from Results where student=?',
                        (id,))
     results = [dict(quiz=row[0],grade=row[1]) for row in cur.fetchall()]
     if not results:
         msg = 'No results'
     return render_template('student_results.html',results=results,msg=msg)

@app.route('/quiz/add', methods=['GET','POST'])
def add_quiz():
     if request.method == 'POST':
         if not session.get('logged_in'):
             abort(401)
         g.db.execute('insert into Quizzes (subject'\
                                      ', questions, testDate) '\
                                      'values (?, ?, ?)',
                      [request.form['subject']
                       , request.form['questions']
                       , request.form['testDate']])
         g.db.commit()
         flash('New quiz successfully posted')
         return redirect(url_for('show_entries'))
     return render_template('add_quiz.html')

@app.route('/results/add', methods=['GET','POST'])
def add_result():
    cur1 = g.db.execute('select id from Students')
    students = [dict(ID=row[0]) for row in cur1.fetchall()]
    cur2 = g.db.execute('select di from Quizzes')
    quizzes = [dict(ID=row[0]) for row in cur2.fetchall()]
    if request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)
        g.db.execute(
    'insert into Results (quiz,student,grade) values (?,?,?)',
            (
                request.form.get('Quiz'),
                request.form.get('Student'),
                request.form.get('grade')
            )
        )
        g.db.commit()
        flash('New result successfully posted')
        return redirect(url_for('show_entries'))
    return render_template('add_result.html',students=students,quizzes=quizzes)

if __name__ == '__main__':
    app.run()