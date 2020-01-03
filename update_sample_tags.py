#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 09:13:28 2020

@author: antony
"""

import psycopg2
import json

config = json.load(open('edbw/settings.json', 'r'))


connection = psycopg2.connect(user = config['postgresql']['user'],
                              password = config['postgresql']['password'],
                              host = config['postgresql']['host'],
                              port = config['postgresql']['port'],
                              database = config['postgresql']['name'])

cursor = connection.cursor()

cursor.execute("SELECT sample_id, tag_id, tag_type_id, str_value, int_value, float_value FROM sample_tags ORDER BY id")
records = cursor.fetchall()

sql = 'UPDATE sample_tags SET json = %s WHERE sample_id = %s and tag_id = %s'

inserts = []
i = 1
for row in records:
    t = row[2]
    
    if t == 2:
        v = int(row[4])
    elif t == 3:
        v = float(row[5])
    else:
        v = row[3]
    
    j = (json.dumps({'id':row[1], 'value':v}), row[0], row[1], )
    inserts.append(j)
    
    if i % 1000 == 0:
        print('Processed', i)
        #break
        
    i += 1

print('Inserting...')
cursor.executemany(sql, inserts)
 
connection.commit()
cursor.close()
connection.close()