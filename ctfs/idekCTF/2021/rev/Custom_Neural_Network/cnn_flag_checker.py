import numpy as np
import tensorflow as tf

def Float32Equal(a,b):
    return np.abs(a - b) < np.finfo(np.float32).eps

def CheckImage(image, model_filename='flag_model.h5'):
    if not Float32Equal(np.max(image), 1.0):
        return False
    if not Float32Equal(np.min(image), -1.0):
        return False
    model = tf.keras.models.load_model(model_filename)
    input_image = image.copy()
    input_image = np.delete(input_image, range(0,61,10), axis=1)
    input_image = np.delete(input_image, range(0,61,10), axis=0)
    input_image = np.expand_dims(input_image, axis=0)
    return Float32Equal(model.predict([input_image])[0,0,0,0], 2916)
