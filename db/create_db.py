import sqlite3
import os

def setup_db():
    if not os.path.exists('votes.db'):
        open('votes.db', 'w').close()

    conn = sqlite3.connect('votes.db')
    cursor = conn.cursor()

    print('Created votes.db')

    with open('schema.sql', 'r') as f:
        schema = f.read()

    # Check if the Votes table exists
    cursor.execute("PRAGMA table_info('Votes')")
    table_info = cursor.fetchall()
    if len(table_info) > 0:
        print("The Votes table already exists in the database")
    else:
        cursor.executescript(schema)
        print("The Votes table was created successfully")

    conn.commit()
    conn.close()
