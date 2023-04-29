import numpy as np
from PIL import Image

def predict_class(interpreter, image_bytes, food_list):

    # Get input and output tensors
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Load and preprocess image
    img = Image.open(image_bytes).convert('RGB')
    width, height = img.size
    if max(width, height) > 1024:
        resample=Image.BICUBIC
    else:
        resample=Image.BILINEAR

    img = img.resize((input_details[0]['shape'][1], input_details[0]['shape'][2]), resample=resample)
    img = np.array(img, dtype=np.float32) / 255.0

    # Set input tensor
    interpreter.set_tensor(input_details[0]['index'], np.expand_dims(img, axis=0))

    # Run inference
    interpreter.invoke()

    # Get output tensor and index of predicted class
    output_data = interpreter.get_tensor(output_details[0]['index'])
    pred_index = np.argmax(output_data)

    # Get predicted class name and confidence
    pred_value = food_list[pred_index]
    percentage = f"{output_data[0][pred_index]:.0%}"

    return {"prediction": pred_value, "confidence": percentage}
