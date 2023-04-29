from keras.backend import clear_session
from keras.utils import load_img, img_to_array
import tensorflow as tf

def predict_class(model, image, food_list):
    img = load_img(image, target_size=(224, 224))
    img = img_to_array(img)
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)

    pred = model.predict(tf.expand_dims(img, axis=0), batch_size=1)
    index = tf.argmax(pred, axis=-1).numpy()[0]
    index_value = pred[0][index]

    pred_value = food_list[index]

    percentage = f"{index_value:.0%}"

    clear_session()

    return {"prediction": pred_value, "confidence": percentage}


### PREDICTION FUNCTION to be used with tflite_runtime
### Pip install tflite_runtime
### DOES_NOT_WORK WITH PYTHON 3.11 OR 3.10 - USE PYTHON 3.9 OR 3.6

# import numpy as np
# from PIL import Image

# from common.common import food_list

# def predict_class(interpreter, image_bytes):

#     interpreter.allocate_tensors()

#     # Get input and output tensors
#     input_details = interpreter.get_input_details()
#     output_details = interpreter.get_output_details()

#     # Load image and resize to model input shape
#     img = Image.open(image_bytes).convert('RGB').resize((input_details[0]['shape'][1], input_details[0]['shape'][2]), resample=Image.BILINEAR)
#     img = np.array(img).astype(np.float32) / 255.0

#     # Set input tensor
#     interpreter.set_tensor(input_details[0]['index'], np.expand_dims(img, axis=0))

#     # Run inference
#     interpreter.invoke()

#     # Get output tensor and index of predicted class
#     output_data = interpreter.get_tensor(output_details[0]['index'])
#     pred_index = np.argmax(output_data)

#     # Get predicted class name and confidence
#     food_list.sort()
#     pred_value = food_list[pred_index]
#     percentage = "{:.0%}".format(output_data[0][pred_index])

#     return {"prediction": pred_value, "confidence": percentage}
