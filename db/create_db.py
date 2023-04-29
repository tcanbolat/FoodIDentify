import sqlite3
import os

def setup_db():
    if not os.path.exists('db/votes.db'):
        open('db/votes.db', 'w').close()
        print(' * Created votes.db')

    print(' * Connecting to votes.db')
    conn = sqlite3.connect('db/votes.db')
    cursor = conn.cursor()


    with open('db/schema.sql', 'r') as f:
        schema = f.read()

    cursor.execute("PRAGMA table_info('Votes')")
    table_info = cursor.fetchall()
    if len(table_info) > 0:
        print(" * The Votes table already exists in the database")
    else:
        cursor.executescript(schema)
        print(" * The Votes table was created successfully")

    print(' * Closing connection')
    conn.commit()
    conn.close()
