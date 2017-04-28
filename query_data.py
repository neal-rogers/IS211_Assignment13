#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This program queries a database."""

import sqlite3 as lite
import sys

con = lite.connect('pets.db')

with con:
    cur = con.cursor()
    while True:
        id = raw_input('Enter user id: ')

        if id >= 0:
            cur.execute('SELECT p.first_name, p.last_name, p.age, pt.name, '
                        'pt.breed, pt.age as pt_age, pt.dead '
                        'FROM person as p, pet as pt, person_pet as perpet '
                        'WHERE p.id=? AND perpet.person_id == p.id '
                        'AND pt.id == perpet.pet_id', (id))
            db_data = cur.fetchall()

            for i in db_data:
                first_name = i[0]
                last_name = i[1]
                age = i[2]
                pet_name = i[3]
                pet_type = i[4]
                pet_age = i[5]
                living = i[6]

                print ('{} {}, who is {} years old, has a {} named {} who is years old.').format(
                    first_name, last_name, age, pet_type, pet_name, pet_age
                )
        else:
            print "Exiting program..."
            break