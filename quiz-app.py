#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This program does stuff."""

import sqlite3
from flask import Flask, render_template, request, redirect
app = Flask(__name__)


def connect_db():
    return sqlite3.connect(app.config['hw13.db'])

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