import sqlite3
import os

if not os.path.exists('votes.db'):
    open('votes.db', 'w').close()

conn = sqlite3.connect('votes.db')
cursor = conn.cursor()

with open('schema.sql', 'r') as f:
    schema = f.read()
    cursor.executescript(schema)

conn.commit()
conn.close()
print('_DB_Created_')
