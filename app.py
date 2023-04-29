from common.common import food_list, get_latest_file
from config import config
from db.create_db import setup_db
from db.vote import cast_vote
from flask import Flask, render_template, request, make_response
from io import BytesIO
from keras.models import load_model  # REMOVE IMPORT IF USING tflite_runtime
import os
from predict import predict_class

########################################################################
file = get_latest_file('model', 'model')  # REMOVE STATMENT IF USING tflite_runtime
food_model = load_model(file)  # REMOVE STATMENT IF USING tflite_runtime
########################################################################
### LOAD A TFLITE MODEL TO BE USED WITH tflite_runtime package
### Pip install tflite_runtime
### DOES_NOT_WORK WITH PYTHON 3.11 OR 3.10 - USE PYTHON 3.9 OR 3.6

# import tflite_runtime.interpreter as tflite
# model_path = 'model/food_model.tflite'
# food_model = tflite.Interpreter(model_path=model_path)
# food_model.allocate_tensors()
########################################################################

food_list.sort() # Sort food_llist once instead of each prediction



def create_app():
    app = Flask(__name__)
    env = os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config[env])

    return app

app = create_app()

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

            predicted_obj = predict_class(food_model, image, food_list)

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

    data = cast_vote(col_name)

    return make_response({'message': 'New vote submitted successfully!', 'result': data}, 201)


if not os.path.exists('db/votes.db'):
    setup_db()

if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') != 'production':
        app.run(host='0.0.0.0', port=5000, debug=True)
