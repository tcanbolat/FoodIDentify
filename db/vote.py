import sqlite3

def cast_vote(col_name):
    conn = sqlite3.connect('db/votes.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Votes ({}) VALUES (?)".format(col_name),(True,))

    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM Votes WHERE correct = 1")
    correct_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Votes WHERE incorrect = 1")
    incorrect_count = cursor.fetchone()[0]

    conn.close()

    total_count = correct_count + incorrect_count

    if total_count == 0:
        accuracy = 'N/A'
    else:
        accuracy = (correct_count / total_count) * 100
        accuracy = '{:.0f}%'.format(accuracy)

    data = {
        'correct_count': correct_count,
        'incorrect_count': incorrect_count,
        'total_count': total_count,
        'accuracy': accuracy
    }

    return data
