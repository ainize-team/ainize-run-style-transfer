from flask import Flask, request, send_file
from flask_limiter import Limiter
from PIL import Image, ImageOps
from imageLoader import load_img, tensor_to_image

import tensorflow as tf
import tensorflow_hub as hub

hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 8

limiter = Limiter(
  app,
  default_limits=['1 per second']
)

@app.route('/transfer', methods=['POST'])
def transfer():
  if not request.files.get('baseImage'):
    return {'error': 'must have a baseImage'}, 400
  if not request.files.get('styleImage'):
    return {'error': 'must have a styleImage'}, 400

  try:
    baseImage = Image.open(request.files['baseImage'].stream)
    styleImage = Image.open(request.files['styleImage'].stream)

    if(baseImage.format not in ['JPG', 'JPEG', 'PNG']):
      return {'error': 'image must be jpg, jpeg or png'}, 400

    if(styleImage.format not in ['JPG', 'JPEG', 'PNG']):
      return {'error': 'image must be jpg, jpeg or png'}, 400

    baseImage = load_img(baseImage)
    styleImage = load_img(styleImage)

    stylized_image = hub_module(tf.constant(baseImage), tf.constant(styleImage))[0]

    output = tensor_to_image(stylized_image)

    return send_file(output, mimetype='image/png')
  except Exception:
    return {'error': 'can not load your image files. check your image files'}, 400

@app.route('/healthz')
def health():
  return "ok"

@app.errorhandler(413)
def request_entity_too_large(error):
  return {'error': 'File Too Large'}, 413

if __name__ == '__main__':
  app.run(debug=False, port=80, host='0.0.0.0')
