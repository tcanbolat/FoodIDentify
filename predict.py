from common.common import food_list
from keras.backend import clear_session
from keras.utils import load_img, img_to_array
import numpy as np

def predict_class(model, image):
    img = load_img(image, target_size=(224, 224))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img /= 235.

    pred = model.predict(img)
    index = np.argmax(pred)
    index_value = np.max(pred)

    food_list.sort()
    pred_value = food_list[index]

    percentage = "{:.0%}".format(index_value)

    clear_session()

    return {"prediction": pred_value, "confidence": percentage}

