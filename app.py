from common.common import food_list, get_latest_file
from flask import Flask, render_template, request
from io import BytesIO
import os
from predict import predict_class
from keras.models import load_model

app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD=True
)

@app.route('/')
def hello():

    for i in range(len(food_list)):
        food_list[i] = food_list[i].replace("_", " ")

    return render_template('index.html', food_list=food_list)


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

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
