from common.common import food_list, get_latest_file
from db.create_db import setup_db
from flask import Flask, render_template, request, make_response
from io import BytesIO
from keras.backend import clear_session
from keras.models import load_model
import os
from predict import predict_class
import sqlite3


app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD=True
)

@app.route('/')
def hello():

    for i in range(len(food_list)):
        food_list[i] = food_list[i].replace("_", " ")

    return render_template('main.html', food_list=food_list)


@app.route('/predict', methods=['POST'])
def predict_image():
    if request.method == 'POST':
        f = request.files['file']
        image = BytesIO(f.read())

        if image:

            file = get_latest_file('model', 'model')
            food_model = load_model(file)

            predicted_obj = predict_class(food_model, image)

            return {"prediction": predicted_obj}


@app.route('/vote', methods=['POST'])
def submit_vote():

    new_vote = request.get_json()

    if 'correct' in new_vote:
            col_name = 'correct'
    elif 'incorrect' in new_vote:
            col_name = 'incorrect'
    else:
        response = make_response({'message': 'Could not cast vote.'}, 400)
        return response

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

    return make_response({'message': 'New vote submitted successfully', 'result': data}, 201)


if not os.path.exists('db/votes.db'):
    setup_db()

clear_session()

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
