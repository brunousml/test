import json

import os
from flask import Flask, request, render_template, flash, url_for
from flask_cors import CORS
from werkzeug.utils import redirect, secure_filename

from core.reader import text_extractor
from core.nlu import insights

UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
  filename = ""
  if request.method == 'POST':

    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)

    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

  result = insights(text_extractor(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
  return render_template('results.html', result=result)


@app.route('/')
def home():
  return render_template('index.html')


@app.route('/results')
def results():
  return render_template('results.html')


@app.route('/market')
def market():
  return render_template('market.html')


@app.route('/compare')
def compare():
  return render_template('compare.html')



port = int(os.getenv('PORT', 8000))

if __name__ == '__main__':
  app.secret_key = 'super secret key'
  app.config['SESSION_TYPE'] = 'filesystem'
  app.debug = True
  app.run(host='0.0.0.0', port=port, debug=True)
