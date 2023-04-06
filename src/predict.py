import tensorflow as tf
from keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt

def txt_to_list(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        lst = [line.strip() for line in lines]
    return lst

def predict_class(model, images, show = True):
  for img in images:
    img = tf.keras.preprocessing.image.load_img(img, target_size=(235, 235))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img /= 235.

    pred = model.predict(img)
    index = np.argmax(pred)

    food_list = txt_to_list('meta/classes.txt')
    food_list.sort()
    pred_value = food_list[index]

    if show:
        plt.imshow(img[0])
        plt.axis('off')
        plt.title(pred_value)
        plt.show()

images = []
images.append('BD13D8BA-9BFA-4BFD-AF09-17DC38CBFECA.jpg')

food_model = load_model("model/food_model_small_96_percent.h5")

predict_class(food_model, images, True)
