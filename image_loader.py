from PIL import Image, ImageOps
import numpy as np

import tensorflow as tf
import tensorflow.keras

import numpy as np
import PIL.Image
import io

def load_img(img):
  byte_io = io.BytesIO()
  img.save(byte_io, format='PNG')
  byte_arr = byte_io.getvalue()

  img = tf.image.decode_image(byte_arr, channels=3)
  img = tf.image.convert_image_dtype(img, tf.float32)

  shape = tf.cast(tf.shape(img)[:-1], tf.float32)
  max_dim = 512
  long_dim = max(shape)
  scale = max_dim / long_dim

  new_shape = tf.cast(shape * scale, tf.int32)

  img = tf.image.resize(img, new_shape)
  img = img[tf.newaxis, :]
  return img

def tensor_to_image(tensor):
  tensor = tensor * 255
  tensor = np.array(tensor, dtype=np.uint8)

  if np.ndim(tensor) > 3:
    assert tensor.shape[0] == 1
    tensor = tensor[0]
  
  output = PIL.Image.fromarray(tensor)
  img_io = io.BytesIO()
  output.save(img_io, 'PNG', quality=70)
  img_io.seek(0)
  
  return img_io
