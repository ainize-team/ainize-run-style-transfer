from flask import Flask, request, send_file
from flask_limiter import Limiter
from PIL import Image, ImageOps
import numpy as np

import tensorflow as tf
import tensorflow.keras

import numpy as np
import PIL.Image
import io
import tensorflow_hub as hub

hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

def load_img(img):
  byteIO = io.BytesIO()
  img.save(byteIO, format='PNG')
  byteArr = byteIO.getvalue()

  img = tf.image.decode_image(byteArr, channels=3)
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
  tensor = tensor*255
  tensor = np.array(tensor, dtype=np.uint8)

  if np.ndim(tensor)>3:
    assert tensor.shape[0] == 1
    tensor = tensor[0]
  return PIL.Image.fromarray(tensor)

app = Flask(__name__) 
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 8

limiter = Limiter(
    app,
    default_limits=['1 per second']
)

@app.route('/transfer', methods=['POST'])
def transfer():
    ## check isImage
    
    if not request.files.get('baseImage'):
        return { 'error': 'must have a baseImage' }, 400
    if not request.files.get('styleImage'):
        return { 'error': 'must have a styleImage' }, 400

    try:
        baseImage = Image.open(request.files['baseImage'].stream)
        styleImage = Image.open(request.files['styleImage'].stream)

        if(baseImage.format not in ['JPG', 'JPEG', 'PNG']):
            return { 'error': 'image must be jpg, jpeg or png' }, 400

        if(styleImage.format not in ['JPG', 'JPEG', 'PNG']):
            return { 'error': 'image must be jpg, jpeg or png' }, 400

        baseImage = load_img(baseImage)
        styleImage = load_img(styleImage)

        stylized_image = hub_module(tf.constant(baseImage), tf.constant(styleImage))[0]

        output = tensor_to_image(stylized_image)

        img_io = io.BytesIO()
        output.save(img_io, 'JPEG', quality=70)
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')

    except Exception :
        return { 'error': 'can not load your image files. check your image files' }, 400

@app.route('/healthz')
def health():
    return "ok"

@app.errorhandler(413)
def request_entity_too_large(error):
    return { 'error': 'File Too Large' }, 413

if __name__ == '__main__':
    app.run(debug=False, port=80, host='0.0.0.0')
