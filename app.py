from common.common import food_list, get_latest_file
from db import create_db, vote
from flask import Flask, render_template, request, make_response
from io import BytesIO
from keras.backend import clear_session  # REMOVE IMPORT IF USING tflite_runtime
from keras.models import load_model  # REMOVE IMPORT IF USING tflite_runtime
import os
from predict import predict_class



app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD=True
)

file = get_latest_file('model', 'model')  # REMOVE STATMENT IF USING tflite_runtime
food_model = load_model(file)  # REMOVE STATMENT IF USING tflite_runtime

food_list.sort() # Sort food_llist once instead of each prediction


########################################################################
### LOAD A TFLITE MODEL TO BE USED WITH tflite_runtime package
### Pip install tflite_runtime
### DOES_NOT_WORK WITH PYTHON 3.11 OR 3.10 - USE PYTHON 3.9 OR 3.6

# import tflite_runtime.interpreter as tflite
# model_path = 'model/food_model.tflite'
# food_model = tflite.Interpreter(model_path=model_path)
# food_model.allocate_tensors()
########################################################################


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

    data = vote.submit_vote(col_name)

    return make_response({'message': 'New vote submitted successfully', 'result': data}, 201)


if not os.path.exists('db/votes.db'):
    create_db.setup_db()

clear_session()  # REMOVE STATMENT IF USING tflite_runtime

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
