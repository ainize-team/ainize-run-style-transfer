from flask import Flask, request, send_file
from flask_limiter import Limiter
from PIL import Image, ImageOps
from image_loader import load_img, tensor_to_image

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
  if not request.files.get('base_image'):
    return {'error': 'must have a base image'}, 400
  if not request.files.get('style_image'):
    return {'error': 'must have a style image'}, 400

  try:
    base_image = Image.open(request.files['base_image'].stream)
    style_image = Image.open(request.files['style_image'].stream)

    if(base_image.format not in ['JPG', 'JPEG', 'PNG']):
      return {'error': 'image must be jpg, jpeg or png'}, 400

    if(style_image.format not in ['JPG', 'JPEG', 'PNG']):
      return {'error': 'image must be jpg, jpeg or png'}, 400

    base_image = load_img(base_image)
    style_image = load_img(style_image)

    stylized_image = hub_module(tf.constant(base_image), tf.constant(style_image))[0]

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
