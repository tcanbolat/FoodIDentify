from flask import Flask, render_template, request
from io import BytesIO
from predict import predict_class
from keras.models import load_model

app = Flask('image-recognition-model')


@app.route('/')
def hello():

    def txt_to_list(filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            lst = [line.strip().replace('_', ' ') if '_' in line else line.strip() for line in lines]
        return lst

    return render_template('index.html', food_list=txt_to_list('meta/classes_small.txt'))


@app.route('/predict', methods=['POST'])
def predict_image():
    if request.method == 'POST':
        f = request.files['file']
        image = BytesIO(f.read())

        if image:
            images = []
            images.append(image)
            food_model = load_model("model/food_model_small_96_percent.h5")

            predicted_value = predict_class(food_model, images, False)

            return {"prediction": predicted_value}
