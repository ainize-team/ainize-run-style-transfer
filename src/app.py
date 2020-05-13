from flask import Flask, request, send_file
from flask_limiter import Limiter
from PIL import Image, ImageOps
from style_transfer import stylize_img
from ga import track_event

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 8

limiter = Limiter(app, default_limits=['1 per second'])

@app.route('/transfer', methods=['POST'])
def transfer():
  track_event(category='Style_Transfer', action='transfer')

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

    stylized_image = stylize_img(base_image, style_image)

    return send_file(stylized_image, mimetype='image/png')
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
