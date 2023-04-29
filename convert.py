import tensorflow as tf

def convert_to_tflite(model_path, tflite_path):
    # Load the model
    model = tf.keras.models.load_model(model_path)

    # Convert the model to TFLite format
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    # Save the TFLite model
    with open(tflite_path, 'wb') as f:
        f.write(tflite_model)

model_path = 'path/to/my_model.h5'
tflite_path = 'path/to/my_model.tflite' #path you want to .tflite file to be once converted

convert_to_tflite(model_path, tflite_path)
