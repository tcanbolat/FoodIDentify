# from common.common import food_list
# from keras.backend import clear_session
# from keras.utils import load_img, img_to_array
# import numpy as np

# def predict_class(model, image):
#     img = load_img(image, target_size=(224, 224))
#     img = img_to_array(img)
#     img = np.expand_dims(img, axis=0)
#     img /= 235.

#     pred = model.predict(img)
#     index = np.argmax(pred)
#     index_value = np.max(pred)

#     food_list.sort()
#     pred_value = food_list[index]

#     percentage = "{:.0%}".format(index_value)

#     clear_session()

#     return {"prediction": pred_value, "confidence": percentage}


import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite

from common.common import food_list

def predict_class(image_bytes):
    model_path = 'model/food_model.tflite'
    # Load TFLite model
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    # Get input and output tensors
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Load image and resize to model input shape
    img = Image.open(image_bytes).convert('RGB').resize((input_details[0]['shape'][1], input_details[0]['shape'][2]), resample=Image.BILINEAR)
    img = np.array(img).astype(np.float32) / 255.0

    # Set input tensor
    interpreter.set_tensor(input_details[0]['index'], np.expand_dims(img, axis=0))

    # Run inference
    interpreter.invoke()

    # Get output tensor and index of predicted class
    output_data = interpreter.get_tensor(output_details[0]['index'])
    pred_index = np.argmax(output_data)

    # Get predicted class name and confidence
    food_list.sort()
    pred_value = food_list[pred_index]
    percentage = "{:.0%}".format(output_data[0][pred_index])

    # Clean up
    interpreter.close()

    return {"prediction": pred_value, "confidence": percentage}
