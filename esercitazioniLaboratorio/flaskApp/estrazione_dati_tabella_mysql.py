#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 14:14:54 2022

@author: apirodd
"""

import mysql.connector

config = {
  'user': 'root',
  'password': 'root',
  'host': '127.0.0.1',
  'port': 8889,
  'database': 'BucketList',
  'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)

cursor = cnx.cursor(dictionary=True)

cursor.execute('SELECT `user_id`, `user_name` FROM `tbl_user`')

results = cursor.fetchall()

for row in results:
  id = row['user_id']
  title = row['user_name']
  print ('%s | %s' % (id, title))


cnx.close()